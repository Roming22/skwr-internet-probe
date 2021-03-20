#!/bin/bash
SCRIPT_DIR="$(dirname "$(realpath "$0")")"

DEFAULT="${SCRIPT_DIR}/k8s/config.default"
SECRET="${SCRIPT_DIR}/k8s/config.secret"
for CONFIG in "${DEFAULT}" "${SECRET}"; do
	[[ -e "${CONFIG}" ]] && source "${CONFIG}"
done
unset CONFIG

ask(){
	local TYPE="$1"
	local MODE="$2"
	local VAR="$3"
	local PROMPT="$4"

	local DEFAULT
	local PAD
	local INPUT
	local READ_ARGS

	[[ -n "${!VAR}" ]] && DEFAULT="${!VAR}" || unset DEFAULT

	case "$TYPE" in
		value)
			PROMPT="${PROMPT}$([[ -n "${DEFAULT}" ]] && echo -e " [${DEFAULT}]")"
			;;
		secret)
			READ_ARGS="-s"
			PROMPT="${PROMPT}$([[ -n "${DEFAULT}" ]] && echo -e " [press enter to use existing value]")"
			;;
		*)
			echo "Unsupported type: $TYPE" >&2
			exit 1
			;;
	esac
	case "$MODE" in
		mandatory) ;;
		optional)
			PAD="-"
			;;
		*)
			echo "Unsupported mode: $MODE" >&2
			exit 1
			;;
	esac

	read ${READ_ARGS} -p "${PROMPT}: " INPUT

	case "$TYPE" in
		secret)
			echo
			INPUT="$( echo -n "${INPUT}" | base64  | tr -d '\n' )"
			;;
	esac
	export $VAR="${INPUT:-$DEFAULT}"
	[[ -z "${!VAR}${PAD}" ]] && echo "Invalid value: Do not leave blank" && exit 1
	VAR_LIST="${VAR_LIST} ${VAR}"
}

write_secret(){
    VAR_LIST=( $VAR_LIST )
    for VAR in ${VAR_LIST[@]}; do
        echo "$VAR=${!VAR}"
    done > $SECRET
}

create_secret(){
	ask value mandatory MODEMS_IP_PORT "Enter the list of modems IP:PORT to monitor"
	ask value mandatory MAIL_FROM "Enter the sender email"
	ask value mandatory MAIL_TO "Enter the recipient email"
	ask secret mandatory API_KEY "Enter the SendGrid API key"
	write_secret
}

process_templates(){
	for TEMPLATE in $(find "${SCRIPT_DIR}/k8s" -name \*.in); do
		TARGET="$(echo "${TEMPLATE}" | sed "s:in$:yml.secret:")"
		envsubst < $TEMPLATE > $TARGET
	done
}

create_secret
process_templates
