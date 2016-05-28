;;;;;;;;;;;;;
;; init.el ;;
;;;;;;;;;;;;;
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

;;;;;;;;;;;;;;;;;;;;;
;; General Setting ;;
;;;;;;;;;;;;;;;;;;;;;
;; Hide menu bar
(menu-bar-mode -1)

;; Display Column number
(column-number-mode t)

;; Display line number
(global-linum-mode t)

;; Emphasize parenthesis
(show-paren-mode 1)

;; Key-bind to move on window
(global-set-key (kbd "C-c <left>")  'windmove-left)
(global-set-key (kbd "C-c <down>")  'windmove-down)
(global-set-key (kbd "C-c <up>")    'windmove-up)
(global-set-key (kbd "C-c <right>") 'windmove-right)

;; Undisplay startup message
(setq inhibit-startup-screen -1)

;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Auto install setting ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;
;; auto-install setting
(add-to-list 'load-path (expand-file-name "~/.emacs.d/auto-install/"))
(require 'auto-install)
;; To get package from emacs wiki
(auto-install-update-emacswiki-package-name t)
(auto-install-compatibility-setup)

;;;;;;;;;;;;;;;;;;;
;; gdb setting   ;;
;;;;;;;;;;;;;;;;;;;
(setq gdb-many-windows t)

;;; 変数の上にマウスカーソルを置くと値を表示
(add-hook 'gdb-mode-hook '(lambda () (gud-tooltip-mode t)))

;;; I/O バッファを表示
(setq gdb-use-separate-io-buffer t)

;;; t にすると mini buffer に値が表示される
(setq gud-tooltip-echo-area nil)

;;;;;;;;;;;;;;;;;;;
;; magit setting ;;
;;;;;;;;;;;;;;;;;;;
(add-to-list 'load-path "~/.emacs.d/elpa/dash-2.12.0/")
(load-library "dash")
(add-to-list 'load-path "~/.emacs.d/elisp/with-editor")
(require 'with-editor)
(add-to-list 'load-path "~/.emacs.d/elisp/magit/lisp")
(require 'magit)

