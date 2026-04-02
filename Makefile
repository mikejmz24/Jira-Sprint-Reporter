# Test the application
# Usage:
#   make test                     → all tests  (compact: key error line per failure)
#   make test auth                → tests/auth/ only
#   make test auth test_login     → filtered by keyword
#   V=1 make test [...]           → verbose: full multi-line diff details
test:
	@path="tests/"; filter=""; tb="short"; \
	if [ -n "$(word 2,$(MAKECMDGOALS))" ]; then \
		path="tests/$(word 2,$(MAKECMDGOALS))/"; \
	fi; \
	if [ -n "$(word 3,$(MAKECMDGOALS))" ]; then \
		filter="-k $(word 3,$(MAKECMDGOALS))"; \
	fi; \
	if [ "$(V)" = "1" ]; then tb="long"; fi; \
	pytest -v --tb=$$tb --no-header -rN $$filter $$path 2>&1 | \
	awk -v verbose="$(V)" '\
		BEGIN { tc=0; fc=0; in_fail=0; cur_fail=""; cur_det=""; summary="" } \
		\
		/^=+ FAILURES =+/ { in_fail=1; next } \
		/^=+ ERRORS =+/   { in_fail=1; next } \
		/^=+ short test summary/ { \
			if (cur_fail!="") det[cur_fail]=cur_det; \
			in_fail=0; next \
		} \
		\
		/^=+[[:space:]].*[0-9]+.*[smh]/ { \
			tmp=$$0; sub(/^=+[[:space:]]/, "", tmp); sub(/[[:space:]]=+$$/, "", tmp); \
			summary=tmp; next \
		} \
		/^=+/ { in_fail=0; next } \
		\
		in_fail && /^_+[[:space:]][A-Za-z]/ { \
			if (cur_fail!="") det[cur_fail]=cur_det; \
			tmp=$$0; sub(/^_+[[:space:]]/, "", tmp); sub(/[[:space:]]_+$$/, "", tmp); \
			sub(/^ERROR at setup of /,    "", tmp); \
			sub(/^ERROR at teardown of /, "", tmp); \
			sub(/^ERROR collecting /,     "", tmp); \
			sub(/^[A-Z][a-zA-Z0-9_]*\./, "", tmp); \
			cur_fail=tmp; cur_det=""; next \
		} \
		in_fail && /^E$$/ { next } \
		in_fail && /^E[[:space:]]/ { \
			if ($$0 ~ /^E[[:space:]]*$$/)               { next } \
			if ($$0 ~ /^E[[:space:]]+[?]/)              { next } \
			if ($$0 ~ /At index [0-9]+ diff:/)          { next } \
			if ($$0 ~ /Full diff:/)                     { next } \
			if ($$0 ~ /Use -v/)                         { next } \
			if ($$0 ~ /^E[[:space:]]+\[[[:space:]]*$$/) { next } \
			if ($$0 ~ /^E[[:space:]]+\][[:space:]]*$$/) { next } \
			if ($$0 ~ /^E[[:space:]]+\{[[:space:]]*$$/) { next } \
			if ($$0 ~ /^E[[:space:]]+\}[[:space:]]*$$/) { next } \
			if ($$0 ~ /AssertionError: assert .+ == /) { \
				idx=index($$0," == "); \
				cur_det=cur_det "      [E_ASSERT]" substr($$0,1,idx-1) "[ASSERT_EQ]" substr($$0,idx+4) "\n" \
			} else if ($$0 ~ / != /) { \
				idx=index($$0," != "); \
				cur_det=cur_det "      [E_NEQ]" substr($$0,1,idx-1) "[NEQ]" substr($$0,idx+4) "\n" \
			} else if ($$0 ~ /^E[[:space:]]{3,}-[[:space:]]/) { \
				cur_det=cur_det "      [E_MINUS]" $$0 "\n" \
			} else if ($$0 ~ /[+][[:space:]]+where / || $$0 ~ /[+][[:space:]]+and /) { \
				cur_det=cur_det "      [E_REG]" $$0 "\n" \
			} else if ($$0 ~ /^E[[:space:]]{3,}[+][[:space:]]/) { \
				cur_det=cur_det "      [E_PLUS]" $$0 "\n" \
			} else { \
				cur_det=cur_det "      [E_REG]" $$0 "\n" \
			}; \
			next \
		} \
		in_fail && /^>[[:space:]]/        { cur_det=cur_det "      " $$0 "\n"; next } \
		in_fail && /^[a-zA-Z\/].*:[0-9]+:/ { cur_det=cur_det "      " $$0 "\n"; next } \
		in_fail { next } \
		\
		/::.*[[:space:]](PASSED|FAILED|ERROR|SKIPPED)/ { \
			sub(/[[:space:]]+\[[[:space:]0-9]+%\]$$/, ""); \
			split($$0,p,"::"); file=p[1]; \
			n=split($$0,w," "); status=w[n]; \
			sub(/[[:space:]]*(PASSED|FAILED|ERROR|SKIPPED)$$/, ""); \
			n=split($$0,q,"::"); tname=q[n]; \
			tc++; \
			tfile[tc]=file; tname_a[tc]=tname; tstatus[tc]=status; \
			if (!(file in fseen)) { forder[++fc]=file; fseen[file]=1 } \
			if      (status=="PASSED")  fp[file]++; \
			else if (status=="FAILED")  ff[file]++; \
			else if (status=="ERROR")   fe[file]++; \
			else if (status=="SKIPPED") fs[file]++; \
			next \
		} \
		\
		END { \
			if (cur_fail!="") det[cur_fail]=cur_det; \
			\
			for (fi=1; fi<=fc; fi++) { \
				f=forder[fi]; \
				printf "\n  %s\n", f; \
				for (ti=1; ti<=tc; ti++) { \
					if (tfile[ti]!=f) continue; \
					printf "    [%s] %s\n", tstatus[ti], tname_a[ti]; \
					t=tname_a[ti]; st=tstatus[ti]; \
					if ((st=="FAILED"||st=="ERROR") && t in det) { \
						if (verbose=="1") { \
							printf "%s", det[t] \
						} else { \
							n=split(det[t], dlines, "\n"); \
							for (dl=1; dl<=n; dl++) { \
								if (dlines[dl] ~ /\[E_/) { printf "%s\n", dlines[dl]; break } \
							} \
						} \
					} \
				} \
				parts=""; \
				if (fp[f]) parts=sprintf("[S_PASS]%d passed[END]", fp[f]); \
				if (ff[f]) parts=parts (parts?", ":"") sprintf("[S_FAIL]%d failed[END]", ff[f]); \
				if (fe[f]) parts=parts (parts?", ":"") sprintf("[S_ERR]%d errors[END]", fe[f]); \
				if (fs[f]) parts=parts (parts?", ":"") sprintf("[S_SKIP]%d skipped[END]", fs[f]); \
				printf "    [=>] %s\n", parts \
			} \
			if (summary!="") { \
				out=summary; \
				gsub(/[0-9]+ failed/,    "[T_FAIL]&[END]",  out); \
				gsub(/[0-9]+ passed/,    "[T_PASS]&[END]",  out); \
				gsub(/[0-9]+ error[s]*/, "[T_ERR]&[END]",   out); \
				gsub(/[0-9]+ skipped/,   "[T_SKIP]&[END]",  out); \
				printf "\n  [TOTAL] %s\n\n", out \
			} \
		}' | \
	sed \
		-e 's/\[PASSED\]/\x1b[32m--- PASS\x1b[0m/g' \
		-e 's/\[FAILED\]/\x1b[31m--- FAIL\x1b[0m/g' \
		-e 's/\[ERROR\]/\x1b[31m--- ERROR\x1b[0m/g' \
		-e 's/\[SKIPPED\]/\x1b[33m--- SKIP\x1b[0m/g' \
		-e 's/\[S_PASS\]\([0-9]* passed\)\[END\]/\x1b[32m\1\x1b[0m/g' \
		-e 's/\[S_FAIL\]\([0-9]* failed\)\[END\]/\x1b[31m\1\x1b[0m/g' \
		-e 's/\[S_ERR\]\([0-9]* error[s]*\)\[END\]/\x1b[33m\1\x1b[0m/g' \
		-e 's/\[S_SKIP\]\([0-9]* skipped\)\[END\]/\x1b[2m\1\x1b[0m/g' \
		-e 's/\[=>\]/\x1b[2m=>\x1b[0m/g' \
		-e 's/\[TOTAL\]/\x1b[1mTotal:\x1b[0m/g' \
		-e 's/\[T_FAIL\]\([0-9]* failed\)\[END\]/\x1b[1m\x1b[31m\1\x1b[0m/g' \
		-e 's/\[T_PASS\]\([0-9]* passed\)\[END\]/\x1b[1m\x1b[32m\1\x1b[0m/g' \
		-e 's/\[T_ERR\]\([0-9]* error[s]*\)\[END\]/\x1b[1m\x1b[33m\1\x1b[0m/g' \
		-e 's/\[T_SKIP\]\([0-9]* skipped\)\[END\]/\x1b[2m\1\x1b[0m/g' \
		-e 's/\[E_ASSERT\]\(.*assert \)\(.*\)\[ASSERT_EQ\]\(.*\)/\x1b[38;5;9m\1\x1b[38;5;114m\2\x1b[38;5;9m == \x1b[38;5;210m\3\x1b[0m/' \
		-e 's/\[E_NEQ\]\(.*\)\[NEQ\]\(.*\)/\x1b[38;5;114m\1\x1b[38;5;9m != \x1b[38;5;210m\2\x1b[0m/' \
		-e 's/\[E_MINUS\]\(.*\)/\x1b[38;5;210m\1\x1b[0m/' \
		-e 's/\[E_PLUS\]\(.*\)/\x1b[38;5;114m\1\x1b[0m/' \
		-e 's/\[E_REG\]\(.*\)/\x1b[38;5;9m\1\x1b[0m/' \
		-e '/^      >/s/.*/\x1b[38;5;11m&\x1b[0m/' \
		-e '/^      [a-zA-Z\/].*:[0-9]\{1,\}:/s/.*/\x1b[2m&\x1b[0m/'

%:
	@:

.PHONY: all build run test clean watch migrate seed truncate refresh %
