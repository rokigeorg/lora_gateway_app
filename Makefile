current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
comprun :
        @echo $(current_dir)