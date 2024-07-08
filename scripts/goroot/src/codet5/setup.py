from tree_sitter import Language

Language.build_library(
  # Store the library in the `build` directory
  '/bigdata/qiuhan/codet5/usage/goroot/src/codet5/resources/build/my-languages.so',

  # Include one or more languages
  [
      '/bigdata/qiuhan/codet5/usage/goroot/src/codet5/resources/tree-sitter-go-master'
  ]
)
