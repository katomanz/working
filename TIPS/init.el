;;
;; init.el
;;

;; Language.
(set-language-environment 'Japanese)

;; Coding system.
(set-default-coding-systems 'utf-8)
(set-keyboard-coding-system 'utf-8)
(set-terminal-coding-system 'utf-8)
(set-buffer-file-coding-system 'utf-8)
(prefer-coding-system 'utf-8)

;; Package Manegement
(require 'package)
(add-to-list 'package-archives '("melpa" . "http://melpa.milkbox.net/packages/") t)
(add-to-list 'package-archives '("marmalade" . "http://marmalade-repo.org/packages/"))
(package-initialize)

;; General Setting
;; Hide menu bar
77;10102;0c(menu-bar-mode -1)

;; Display Column number
(column-number-mode t)

;; Display line number
(global-linum-mode t)

;; Emphasize parenthesis
(show-paren-mode 1)

;; auto-install setting
(add-to-list 'load-path (expand-file-name "~/.emacs.d/auto-install/"))
(require 'auto-install)
;; To get package from emacs wiki
(auto-install-update-emacswiki-package-name t)
(auto-install-compatibility-setup)


