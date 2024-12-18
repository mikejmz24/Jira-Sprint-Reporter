run-tests:
	pytest --tb=short --disable-warnings -v test_entities.py 2>&1 | grep -E "^(test_|.* (PASSED|FAILED|ERROR)$)" | grep -vE "^\[|^test_entities.py:[0-9]+: in"

.PHONY: test

# test:
# 	pytest --color=yes --tb=short --disable-warnings -v tests/
# test:
# 	@echo "=== Raw pytest output ==="
# 	pytest --color=yes --tb=short --disable-warnings -v tests/ 2>&1 | head -n 20
# 	@echo "\n=== Trying different grep patterns ==="
# 	pytest --color=yes --tb=short --disable-warnings -v tests/ 2>&1 | grep -E ".*PASSED|.*FAILED|.*ERROR"
# test:
# 	@pytest --color=yes --tb=short --disable-warnings -v tests/ 2>&1 | \
# 		grep -E "^tests/.*\[(.*?)\]" | \
# 		sed -e 's/\[.*\]$$//' \
# 		    -e 's/PASSED$$/\x1b[32mPASSED\x1b[0m/' \
# 		    -e 's/FAILED$$/\x1b[31mFAILED\x1b[0m/' \
# 		    -e 's/ERROR$$/\x1b[91mERROR\x1b[0m/'
	
# test:
# 	@pytest --color=yes --tb=short --disable-warnings -v tests/ 2>&1 | \
# 	awk '                                                                                     \
# 		BEGIN { passed=0; failed=0; errors=0; last_suite = ""; }                             \
# 		/^tests\/.*\[(.*?)\]/ {                                                              \
# 			line = $$0;                                                                      \
# 			if (line ~ /::Test[A-Z]/) {                                                     \
# 				suite = line;                                                               \
# 				sub(/::test_.*$$/, "", suite);                                             \
# 				if (suite != last_suite) {                                                 \
# 					printf "\n=== %s ===\n", suite;                                        \
# 					last_suite = suite;                                                    \
# 				}                                                                          \
# 				sub(/^tests\/[^:]+::Test[^:]+::/, "    ", line);                         \
# 			}                                                                               \
# 			sub(/\[.*\]/, "", line);                                                       \
# 			if ($$0 ~ /PASSED/) {                                                          \
# 				passed++;                                                                  \
# 				printf "%s \033[32mPASSED\033[0m\n", line;                               \
# 			} else if ($$0 ~ /FAILED/) {                                                   \
# 				failed++;                                                                  \
# 				printf "%s \033[31mFAILED\033[0m\n", line;                               \
# 			} else if ($$0 ~ /ERROR/) {                                                    \
# 				errors++;                                                                  \
# 				printf "%s \033[91mERROR\033[0m\n", line;                                \
# 			}                                                                              \
# 		}                                                                                    \
# 		END {                                                                                \
# 			total = passed + failed + errors;                                                \
# 			printf "\n=== Test Summary ===\n";                                               \
# 			printf "Total: %d tests\n", total;                                               \
# 			if (passed > 0) printf "\033[32mPassed: %d\033[0m\n", passed;                   \
# 			if (failed > 0) printf "\033[31mFailed: %d\033[0m\n", failed;                   \
# 			if (errors > 0) printf "\033[91mErrors: %d\033[0m\n", errors;                   \
# 		}'

# test:
# 	@pytest --color=yes --tb=short --disable-warnings -v tests/ 2>&1 | \
# 	awk '                                                                                     \
# 		BEGIN { passed=0; failed=0; errors=0; last_file = ""; last_suite = ""; }             \
# 		/^tests\/.*\[(.*?)\]/ {                                                              \
# 			line = $$0;                                                                      \
# 			file = $$0;                                                                      \
# 			sub(/::.*$$/, "", file);                                                         \
# 			if (file != last_file) {                                                         \
# 				printf "\n=== %s ===\n", file;                                               \
# 				last_file = file;                                                            \
# 				last_suite = "";                                                             \
# 			}                                                                                \
# 			if (line ~ /::Test[A-Z]/) {                                                      \
# 				suite = line;                                                                \
# 				sub(/::test_.*$$/, "", suite);                                               \
# 				if (suite != last_suite) {                                                   \
# 					printf "    === %s ===\n", suite;                                         \
# 					last_suite = suite;                                                       \
# 				}                                                                            \
# 				sub(/^tests\/[^:]+::Test[^:]+::/, "        ", line);                         \
# 			}                                                                                \
# 			sub(/\[.*\]/, "", line);                                                         \
# 			if ($$0 ~ /PASSED/) {                                                            \
# 				passed++;                                                                    \
# 				printf "%s \033[32mPASSED\033[0m\n", line;                                   \
# 			} else if ($$0 ~ /FAILED/) {                                                     \
# 				failed++;                                                                    \
# 				printf "%s \033[31mFAILED\033[0m\n", line;                                   \
# 			} else if ($$0 ~ /ERROR/) {                                                      \
# 				errors++;                                                                    \
# 				printf "%s \033[91mERROR\033[0m\n", line;                                    \
# 			}                                                                                \
# 		}                                                                                    \
# 		END {                                                                                \
# 			total = passed + failed + errors;                                                \
# 			printf "\n=== Test Summary ===\n";                                               \
# 			printf "Total: %d tests\n", total;                                               \
# 			if (passed > 0) printf "\033[32mPassed: %d\033[0m\n", passed;                   \
# 			if (failed > 0) printf "\033[31mFailed: %d\033[0m\n", failed;                   \
# 			if (errors > 0) printf "\033[91mErrors: %d\033[0m\n", errors;                   \
# 		}'

# Default to running all tests
TEST_PATH ?= tests/

# Function to convert filename/pattern to pytest-compatible path
define get_test_path
$(if $(filter %.py,$(1)),tests/$(1),$(if $(filter test_%,$(1)),tests/*$(1)*,tests/*$(1)*))
endef

# Generic test runner with optional file/suite filtering
test:
	@pytest --color=yes --tb=short --disable-warnings -v $(TEST_PATH) 2>&1 | \
	awk '                                                                                     \
		BEGIN { passed=0; failed=0; errors=0; last_file = ""; last_suite = ""; }             \
		/^tests\/.*\[(.*?)\]/ {                                                              \
			line = $$0;                                                                      \
			file = $$0;                                                                      \
			sub(/::.*$$/, "", file);                                                         \
			if (file != last_file) {                                                         \
				printf "\n=== %s ===\n", file;                                               \
				last_file = file;                                                            \
				last_suite = "";                                                             \
			}                                                                                \
			if (line ~ /::Test[A-Z]/) {                                                      \
				suite = line;                                                                \
				sub(/::test_.*$$/, "", suite);                                               \
				if (suite != last_suite) {                                                   \
					printf "    === %s ===\n", suite;                                         \
					last_suite = suite;                                                       \
				}                                                                            \
				sub(/^tests\/[^:]+::Test[^:]+::/, "        ", line);                         \
			}                                                                                \
			sub(/\[.*\]/, "", line);                                                         \
			if ($$0 ~ /PASSED/) {                                                            \
				passed++;                                                                    \
				printf "%s \033[32mPASSED\033[0m\n", line;                                   \
			} else if ($$0 ~ /FAILED/) {                                                     \
				failed++;                                                                    \
				printf "%s \033[31mFAILED\033[0m\n", line;                                   \
			} else if ($$0 ~ /ERROR/) {                                                      \
				errors++;                                                                    \
				printf "%s \033[91mERROR\033[0m\n", line;                                    \
			}                                                                                \
		}                                                                                    \
		END {                                                                                \
			total = passed + failed + errors;                                                \
			printf "\n=== Test Summary ===\n";                                               \
			printf "Total: %d tests\n", total;                                               \
			if (passed > 0) printf "\033[32mPassed: %d\033[0m\n", passed;                   \
			if (failed > 0) printf "\033[31mFailed: %d\033[0m\n", failed;                   \
			if (errors > 0) printf "\033[91mErrors: %d\033[0m\n", errors;                   \
		}'

# Dynamically create test targets for specific files or patterns
test-%:
	$(MAKE) test TEST_PATH=$(call get_test_path,$*)
