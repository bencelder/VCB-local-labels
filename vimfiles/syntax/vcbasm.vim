
"syntax match FooKey   /^[^=]\+/
"syntax match FooValue /[^=]\+$/

"syntax keyword asdf asdf
"hi link asdf Number
"
"
syntax keyword kword symbol macro origin
hi def link kword Keyword

syntax match at_label /@/
hi def link at_label Keyword

syntax match include_kword /%include/
hi def link include_kword Keyword

" The \v at the front removes the need for escape characters
syntax match comment /\v#.*/
hi def link comment Comment

syntax match number_decimal /\v<[0-9]+>/
hi def link number_decimal Number

syntax match number_hex /\v0x[0-9a-fA-F]+/
hi def link number_hex Number

syntax match number_bin /\v0b[01]+/
hi def link number_bin Number


"hi def link value String

"highlight FooKey   ctermfg=cyan guifg=#00ff00
"hi def link FooKey Idenifier
"highlight FooValue ctermfg=red  guifg=#ff0000
