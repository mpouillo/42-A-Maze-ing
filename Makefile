# ==============================================================
#							A_MAZE_ING
# ==============================================================

NAME = a_maze_ing.py

.DEFAULT_GOAL = install

.ONESHELL:
install:
	wget https://cdn.intra.42.fr/document/document/45911/mlx-2.2-py3-ubuntu-any.whl
	unzip -u mlx-2.2-py3-ubuntu-any.whl 
	rm mlx-2.2-py3-ubuntu-any.whl
	rm -rf mlx-2.2.dist-info

run:
	python3 $(NAME)

debug:
	pdb $(NAME)

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

clean:
	rm $(NAME)

fclean: clean
	conda init --reverse
	rm miniconda3
	rm ~/.condarc
	rm -rf ~/.conda

re: fclean install

.PHONY: install run debug clean fclean re
