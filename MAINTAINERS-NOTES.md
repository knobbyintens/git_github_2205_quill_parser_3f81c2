# Quill Parser Service - Maintainer Notes

These maintainer notes belong to the quill parser service. They list the
pending work items that are still open inside the package sources.

## How this file is organised

The Open Action Items section below indexes every pending-work marker that
currently lives inside the `quill` package. A row names the source file, the
line where the marker appears and the marker text itself.

    - [ ] **<path>#<line>** :: <text>

Rows are ordered by file path and then by ascending line number.

### 🧱 Open Action Items

- [ ] **quill/__init__.py#11** :: Publish type stubs for the public facade
- [ ] **quill/__init__.py#12** :: Re-export ParseContext from the package root
- [ ] **quill/__init__.py#13** :: Keep a compatibility shim for the legacy import path
- [ ] **quill/__init__.py#14** :: Check wheel contents in the release workflow
- [ ] **quill/ast_nodes.py#15** :: Give every node a stable identifier
- [ ] **quill/ast_nodes.py#22** :: Limit recursion depth when walking wide trees
- [ ] **quill/ast_nodes.py#32** :: Record whether the import was relative or absolute
- [ ] **quill/ast_nodes.py#40** :: Merge duplicate namespace declarations
- [ ] **quill/ast_nodes.py#41** :: Expose namespace parent links for scope resolution
- [ ] **quill/ast_nodes.py#50** :: Store the resolution result on the reference node
- [ ] **quill/ast_nodes.py#55** :: Flatten should preserve sibling order strictly
- [ ] **quill/ast_nodes.py#63** :: Make name lookup case-insensitive behind a flag
- [ ] **quill/cli.py#13** :: Expose a strict flag consistent with the config object
- [ ] **quill/cli.py#23** :: Print machine readable diagnostics when requested
- [ ] **quill/cli.py#31** :: Exit with a distinct status code for recoverable errors
- [ ] **quill/cli.py#39** :: Support reading source from standard input
- [ ] **quill/config.py#22** :: Validate tab width against encoding assumptions
- [ ] **quill/config.py#23** :: Reject negative depth values at construction time
- [ ] **quill/config.py#24** :: Add environment-variable overrides for CI runs
- [ ] **quill/config.py#35** :: Surface unknown option names with their origin
- [ ] **quill/config.py#36** :: Support reading configuration from TOML payloads
- [ ] **quill/config.py#45** :: Clamp max depth when merging untrusted overrides
- [ ] **quill/config.py#52** :: Hide secret-bearing options from config dumps
- [ ] **quill/emitter.py#11** :: Emit trailing commas for multi-line containers
- [ ] **quill/emitter.py#21** :: Compact single-line namespaces when configured
- [ ] **quill/emitter.py#25** :: Prefer alias spelling when both alias and module exist
- [ ] **quill/emitter.py#30** :: Group imports by origin section when emitting files
- [ ] **quill/emitter.py#36** :: Quote references that clash with python keywords
- [ ] **quill/emitter.py#40** :: Ensure a trailing newline at the end of every module
- [ ] **quill/emitter.py#53** :: Replace tabs with spaces during emission
- [ ] **quill/emitter.py#57** :: Layout comparison should ignore trailing whitespace
- [ ] **quill/errors.py#15** :: Include a severity level in diagnostic records
- [ ] **quill/errors.py#16** :: Render diagnostics as JSON for the command line tool
- [ ] **quill/errors.py#25** :: Attach the offending token to every parse error
- [ ] **quill/errors.py#26** :: Split fatal and recoverable errors into subclasses
- [ ] **quill/errors.py#31** :: Sort diagnostics by line and column before rendering
- [ ] **quill/errors.py#37** :: Group repeated diagnostics by message
- [ ] **quill/errors.py#42** :: Record the phase that produced each diagnostic
- [ ] **quill/lexer.py#23** :: Add a token kind for pragma boundaries
- [ ] **quill/lexer.py#24** :: Carry keyword variants as a separate kind
- [ ] **quill/lexer.py#40** :: Treat annotations as recovery anchors for decorators
- [ ] **quill/lexer.py#46** :: Extract a shared keyword table for lexer reuse
- [ ] **quill/lexer.py#47** :: Detect numeric literals with exponent notation
- [ ] **quill/lexer.py#54** :: Recognise qualified names as a single token
- [ ] **quill/lexer.py#58** :: Track delimiter depth for error snippets
- [ ] **quill/lexer.py#61** :: Reject reversed delimiter pairs early
- [ ] **quill/parser.py#51** :: Add strict mode flag to pragma scanner
- [ ] **quill/parser.py#56** :: Emit source spans for recovery diagnostics
- [ ] **quill/parser.py#63** :: Normalize whitespace in ambiguous literal reports
- [ ] **quill/parser.py#80** :: Retire legacy dollar-prefix handling in pragma scan
- [ ] **quill/parser.py#81** :: Normalize indentation before pragma detection
- [ ] **quill/parser.py#82** :: Drop deprecated strict flag from scanner options
- [ ] **quill/parser.py#88** :: Guard pragma parsing against empty payloads
- [ ] **quill/parser.py#91** :: Record malformed pragma payloads in diagnostics
- [ ] **quill/parser.py#95** :: Reject dollar prefixes in strict parser mode
- [ ] **quill/parser.py#100** :: Remove experimental pragma cache warmup
- [ ] **quill/parser.py#106** :: Skip duplicate pragma directives deterministically
- [ ] **quill/parser.py#140** :: Attach trailing comments to the next node
- [ ] **quill/parser.py#143** :: Normalize whitespace in ambiguous literal reports
- [ ] **quill/parser.py#151** :: Fallback to token stream when lookahead fails
- [ ] **quill/resolver.py#38** :: Document namespace resolution priority
- [ ] **quill/resolver.py#40** :: Strip implicit star imports during resolution
- [ ] **quill/resolver.py#60** :: Merge shadowed aliases deterministically
- [ ] **quill/resolver.py#61** :: Detect duplicate wildcard imports
- [ ] **quill/resolver.py#62** :: Reject aliases that shadow builtin names
- [ ] **quill/resolver.py#68** :: Preserve import grouping in the rebuild pass
- [ ] **quill/resolver.py#72** :: Order relative imports before absolute ones
- [ ] **quill/resolver.py#75** :: Record the original module spelling for audits
- [ ] **quill/resolver.py#79** :: Retire the experimental namespace cache
- [ ] **quill/resolver.py#89** :: Skip builtin names during scope lookup
- [ ] **quill/resolver.py#125** :: Emit a resolution trace at debug level
- [ ] **quill/resolver.py#134** :: Collapse redundant namespace hops
- [ ] **quill/tokenizer.py#14** :: Preserve indentation width as a token attribute
- [ ] **quill/tokenizer.py#27** :: Support escaped quotes inside string literals
- [ ] **quill/tokenizer.py#39** :: Emit zero-width tokens for empty statements
- [ ] **quill/tokenizer.py#43** :: Preserve blank lines as explicit newline tokens
- [ ] **quill/tokenizer.py#44** :: Track the original byte offsets alongside line numbers
- [ ] **quill/tokenizer.py#51** :: Collapse runs of newline tokens when configured
- [ ] **quill/tokenizer.py#55** :: Offer a lossless token render mode
- [ ] **quill/tokenizer.py#56** :: Round-trip tests should compare token spans too

### 📦 Release Checklist

- [ ] Publish 0.7.4 to the internal package index
- [ ] Regenerate the API reference documentation
- [ ] Run the compatibility suite on Python 3.11
