" Don't care about compatibility with vi.
set nocompatible

" Do indentation in a way that is more intelligent than smartindent
filetype plugin indent on

" Turn on syntax coloring for all file types.
syntax on

" Make backspace delete lots of things.
set backspace=indent,eol,start

" Highlight matching parens.
set showmatch

" Do clever things.
set autoindent

"Don't make a # force column zero.
inoremap # X<BS>#

" Enable filetype settings
if has("eval")
        filetype on
        filetype plugin on
        filetype indent on
endif

"
" Apparently I have to add this setting if I want
" to be able to paste more than 50 lines.
"

" read/write a .viminfo file, don't store more
" than 5000 lines of registers
set viminfo='20,\"5000



" Use .tex formatting for .tikz files
autocmd BufNewFile,BufRead *.tikz set filetype=tex



"
" Do some python specific tab stuff.
"

" Expand tabs to four spaces.
autocmd FileType python set tabstop=4
autocmd FileType python set shiftwidth=4

" Make the spaces feel like real tabs.
autocmd FileType python set softtabstop=4

" Expand tabs to spaces.
autocmd FileType python set expandtab


" Do very similar stuff specific to other languages.
autocmd FileType c,h,cpp,hpp,C,H set tabstop=2 shiftwidth=2 softtabstop=2 expandtab


