# Shameless ripoff of the ys theme
#
# Clean, simple, compatible and meaningful.
# Tested on Linux, Unix and Windows under ANSI colors.
# It is recommended to use with a dark background and the font Inconsolata.
# Colors: black, red, green, yellow, *blue, magenta, cyan, and white.
# 
# http://ysmood.org/wp/2013/03/my-ys-terminal-theme/
# Mar 2013 ys

# Machine name.
function box_name {
    [ -f ~/.box-name ] && cat ~/.box-name || echo $HOST
}

# Directory info.
local current_dir='${PWD/#$HOME/~}'

# VCS
YS_VCS_PROMPT_PREFIX1=" %{$FG[135]%}on "
YS_VCS_PROMPT_PREFIX2=":%{$FG[213]%}"
YS_VCS_PROMPT_SUFFIX="%{$reset_color%}"
YS_VCS_PROMPT_DIRTY=" %{$FG[009]%}x"
YS_VCS_PROMPT_CLEAN=" %{$FG[082]%}o"

# Git info.
local git_info='$(git_prompt_info)'
ZSH_THEME_GIT_PROMPT_PREFIX="${YS_VCS_PROMPT_PREFIX1}%{$FG[009]%}git${YS_VCS_PROMPT_PREFIX2}"
ZSH_THEME_GIT_PROMPT_SUFFIX="$YS_VCS_PROMPT_SUFFIX"
ZSH_THEME_GIT_PROMPT_DIRTY="$YS_VCS_PROMPT_DIRTY"
ZSH_THEME_GIT_PROMPT_CLEAN="$YS_VCS_PROMPT_CLEAN"

# HG info
local hg_info='$(ys_hg_prompt_info)'
ys_hg_prompt_info() {
	# make sure this is a hg dir
	if [ -d '.hg' ]; then
		echo -n "${YS_VCS_PROMPT_PREFIX1}hg${YS_VCS_PROMPT_PREFIX2}"
		echo -n $(hg branch 2>/dev/null)
		if [ -n "$(hg status 2>/dev/null)" ]; then
			echo -n "$YS_VCS_PROMPT_DIRTY"
		else
			echo -n "$YS_VCS_PROMPT_CLEAN"
		fi
		echo -n "$YS_VCS_PROMPT_SUFFIX"
	fi
}

# Prompt format: \n # USER at MACHINE in DIRECTORY on git:BRANCH STATE [TIME] \n $ 
PROMPT="
%{$terminfo[bold]$FG[135]%}# \
%{$terminfo[bold]$FG[082]%}%n \
%{$FG[135]%}at \
%{$terminfo[bold]$FG[027]%}$(box_name) \
%{$FG[135]%}in \
%{$terminfo[bold]$FG[214]%}${current_dir}\
${hg_info}\
${git_info} \
%{$reset_color%}%{$FG[255]%}[%*]
%{$terminfo[bold]$FG[009]%}$ %{$reset_color%}"

if [[ "$USER" == "root" ]]; then
PROMPT="
%{$terminfo[bold]$FG[135]%}# \
%{$terminfo[bold]$FG[082]%}%n \
%{$FG[135]%}at \
%{$terminfo[bold]$FG[027]%}$(box_name) \
%{$FG[135]%}in \
%{$terminfo[bold]$FG[214]%}${current_dir}\
${hg_info}\
${git_info} \
%{$FG[255]%}[%*]
%{$terminfo[bold]$FG[009]%}$ %{$reset_color%}"
fi
