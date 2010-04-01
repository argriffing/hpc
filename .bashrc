# ~/.bashrc: executed by bash(1) for non-login shells.
# Much of this is copied from a default Ubuntu .bashrc file.

# add LSF-specific stuff to the path
export PATH=/usr/local/lsf/6.1/linux2.6-glibc2.3-x86/bin:$PATH
export PATH=/usr/local/lsf/6.1/linux2.6-glibc2.3-x86/etc:$PATH

# more LSF stuff
export LSF_BINDIR=/usr/local/lsf/6.1/linux2.6-glibc2.3-x86/bin
export LSF_SERVERDIR=/usr/local/lsf/6.1/linux2.6-glibc2.3-x86/etc
export LSF_LIBDIR=/usr/local/lsf/6.1/linux2.6-glibc2.3-x86/lib
export LD_LIBRARY_PATH=/usr/local/lsf/6.1/linux2.6-glibc2.3-x86/lib
export XLSF_UIDDIR=/usr/local/lsf/6.1/linux2.6-glibc2.3-x86/lib/uid
export LSF_ENVDIR=/usr/local/lsf/conf
export EGO_TOP=/usr/local/lsf
export EGO_BINDIR=/usr/local/lsf/6.1/linux2.6-glibc2.3-x86/bin
export EGO_SERVERDIR=/usr/local/lsf/6.1/linux2.6-glibc2.3-x86/etc
export EGO_LIBDIR=/usr/local/lsf/6.1/linux2.6-glibc2.3-x86/lib
export EGO_CONFDIR=/usr/local/lsf/conf/ego/sam/kernel
export EGO_LOCAL_CONFDIR=/usr/local/lsf/conf/ego/sam/kernel
export EGO_ESRVDIR=/usr/local/lsf/conf/ego/sam/eservice

# add the non-admin installed executable files to the path
export PATH=/brc_share/brc/argriffi/install/bin:$PATH

# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# interactive prompt
PS1="\u@\h:\w/$ "

# continuation interactive prompt
PS2="> "

# don't put duplicate lines in the history. See bash(1) for more options
# don't overwrite GNU Midnight Commander's setting of `ignorespace'.
HISTCONTROL=$HISTCONTROL${HISTCONTROL+,}ignoredups
# ... or force ignoredups and ignorespace
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# color aliases
alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# editor aliases
alias vi='vim'
alias view='vim -R'

# define the default editor
export EDITOR="vim"

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
    . /etc/bash_completion
fi
