# ==============================================================
#							A_MAZE_ING
# ==============================================================

NAME = a_maze_ing

.DEFAULT_GOAL = install

.ONESHELL:
install:
	mkdir -p miniconda3
	wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda3/miniconda.sh
	bash miniconda3/miniconda.sh -b -u -p miniconda3
	rm miniconda3/miniconda.sh
	. miniconda3/bin/activate
	conda init --all
	conda install -c conda-forge xcb-util-keysyms
	export C_INCLUDE_PATH=$(CONDA_PREFIX)/include
	export LIBRARY_PATH=$(CONDA_PREFIX)/lib
	$(MAKE) -C mlx_CLXV

fclean:
	conda init --reverse
	rm miniconda3
	rm ~/.condarc
	rm -rf ~/.conda

re: install clean

.PHONY: install fclean re
