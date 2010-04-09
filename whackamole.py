"""
This module helps to use multiple accessible queues.
"""

class Queue:
    """
    An abstraction of an LSF queue.
    This class does not represent a queue in the traditional sense.
    """
    def __init__(self, name):
        # LSF name of the queue
        self.name = name
        # number of ticks since a job was accepted by the queue
        self.dormancy = 0
        # set of pending job numbers
        self.pending = set()

class Switcher:
    """
    Maintain the state necessary for switching jobs among queues.
    """
    def __init__(self, ordered_queues, fswitch):
        """
        @param ordered_queues: names of queues with the primary queue first
        @param fswitch: a function like fswitch(qname_target, job_number)
        """
        self.queues = [Queue(name) for name in ordered_queues]
        self.fswitch = fswitch

    def on_submission(self, qname_to_jnums):
        """
        Initialize the queue info according to how jobs were submitted.
        @param qname_to_jnums: maps queue name to pending job number set
        """
        self._validate_observed_queues(set(qname_to_jnums))
        # initialize without trying to switch queues
        for queue in self.queues:
            # update the set of pending jobs in the queue
            if queue.name in qname_to_jnums:
                queue.pending = qname_to_jnums[queue.name]
            # update the dormancy
            queue.dormancy = 0

    def on_observation(self, qname_to_jnums):
        """
        Update the queue info.
        @param qname_to_jnums: maps queue name to pending job number set
        """
        self._validate_observed_queues(set(qname_to_jnums))
        # update queue info, including dormancy info.
        for queue in self.queues:
            # get the set of currently pending jobs in the queue
            if queue.name in qname_to_jnums:
                currently_pending = qname_to_jnums[queue.name]
            else:
                currently_pending = set()
            # update the dormancy according to the pending job difference
            if queue.pending - currently_pending:
                queue.dormancy = 0
            else:
                queue.dormancy += 1
            # update the pending jobs in the queue
            queue.pending = currently_pending
        # get queues ready to receive jobs
        target_queues = self._get_target_queues()
        # get jobs ready to switch queues
        mobile_jnums = self._get_mobile_jnums()
        # make a temporary jnum -> queue map
        jnum_to_queue = {}
        for queue in self.queues:
            for j in queue.pending:
                jnum_to_queue[j] = queue
        # Put as many jnums into target queues as possible.
        for q, j in zip(target_queues, mobile_jnums):
            self.fswitch(q.name, j)
        # Update the internal representation of the queues.
        for q, j in zip(target_queues, mobile_jnums):
            jnum_to_queue[j].pending.remove(j)
            q.pending.add(j)

    def _validate_observed_queues(self, observed):
        """
        @param observed: observed queue names
        """
        observed_queue_names = set(observed)
        valid_queue_names = set(q.name for q in self.queues)
        bad_queue_names = observed_queue_names - valid_queue_names
        if bad_queue_names:
            msg = 'unknown queues: ' + ', '.join(bad_queue_names)
            raise Exception(msg)

    def _get_target_queues(self):
        """
        This is a helper function.
        return: the prioritized list of target queues.
        """
        target_queues = []
        # if the primary queue is empty then it is the highest priority target
        if not self.queues[0].pending:
            target_queues.append(self.queues[0])
        # Empty secondary queues are targets,
        # with low dormancy preferred to high dormancy.
        dormancy_queue_pairs = []
        for queue in self.queues:
            if not queue.pending:
                dormancy_queue_pairs.append((queue.dormancy, queue))
        sorted_pairs = list(sorted(dormancy_queue_pairs))
        if sorted_pairs:
            queues = zip(*sorted_pairs)[1]
            target_queues.extend(queues)
        return target_queues

    def _get_mobile_jnums(self):
        """
        This is a helper function.
        return: the prioritized list of footloose job numbers.
        """
        mobile_jnums = []
        # All excess pending jobs in the primary queue are mobile.
        # The largest job ids are most mobile.
        excess = list(reversed(sorted(self.queues[0].pending)))[:-1]
        mobile_jnums.extend(excess)
        # Jobs in high dormancy secondary queues are mobile.
        # Each secondary queue should have at most one pending job.
        dormancy_jnum_pairs = []
        for queue in self.queues[1:]:
            if queue.dormancy:
                pairs = [(queue.dormancy, k) for k in queue.pending]
                dormancy_jnum_pairs.extend(pairs)
        sorted_pairs = list(reversed(sorted(dormancy_jnum_pairs)))
        if sorted_pairs:
            jnums = zip(*sorted_pairs)[1]
            mobile_jnums.extend(jnums)
        return mobile_jnums
