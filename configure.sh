#!/bin/bash
SCRIPT_DIR=`cd $(dirname $0); pwd`

SECRET="$SCRIPT_DIR/etc/secret.env"
[[ -e "$SECRET" ]] && source <(sed -e 's:=:=":' -e 's:$:":' $SECRET)

set_mandatory_value(){
	PROMPT=$2
	VAR=$1
	[[ -n "${!VAR}" ]] && DEFAULT="${!VAR}" || unset DEFAULT
	read -p "$PROMPT`[[ -n "$DEFAULT" ]] && echo -e " [$DEFAULT]"`: " INPUT
	export $VAR="${INPUT:-$DEFAULT}"
	[[ -z "${!VAR}" ]] && echo "Invalid value: Do not leave blank" && exit 1
	VAR_LIST="$VAR_LIST $VAR"
	unset INPUT
}

set_mandatory_password(){
	VAR=$1
	PROMPT=$2
	[[ -n "${!VAR}" ]] && DEFAULT="${!VAR}" || unset DEFAULT
	read -s -p "$PROMPT`[[ -n "$DEFAULT" ]] && echo -e " [leave blank to keep the current value]"`: " INPUT
	echo
	export $VAR="${INPUT:-$DEFAULT}"
	[[ -z "${!VAR}" ]] && echo "Invalid value: Do not leave blank" && exit 1
	VAR_LIST="$VAR_LIST $VAR"
	unset INPUT
}

write_secret(){
    VAR_LIST=( $VAR_LIST )
    for VAR in ${VAR_LIST[@]}; do
        echo "$VAR=${!VAR}"
    done > $SECRET
}

create_secret(){
	set_mandatory_value MAIL_FROM "Enter the sender email"
	set_mandatory_value MAIL_TO "Enter the recipient email"
	set_mandatory_password SENDGRID_API_KEY "Enter the API key for SendGrid"
	write_secret
}

setup_volume(){
    chmod g+w $SCRIPT_DIR/volumes/data
}

create_secret
setup_volume
