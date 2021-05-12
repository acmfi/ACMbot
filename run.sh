#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIRNAME=`basename ${DIR}`
DIRNAME_LW=`echo ${DIRNAME} | awk '{print tolower($0)}'`
NAME=`basename "${0}"`

#
# -> VARS
#

ALIAS="${DIRNAME_LW}"

#
# <- VARS
#



#
# -> FUNCTIONS
#

function print_usage() {
    echo "Usage: ${0} -h | --help"
    echo "Usage: ${0} <-r|--run> | <-s|--stop> | <-c|--clean> | <-l|--log>"
    exit 0
}

function print_help(){

  # http://patorjk.com/software/taag/#p=display&t=ACMbot
	echo -e "\e[94m" '

               █████╗  ██████╗███╗   ███╗██████╗  ██████╗ ████████╗
              ██╔══██╗██╔════╝████╗ ████║██╔══██╗██╔═══██╗╚══██╔══╝
              ███████║██║     ██╔████╔██║██████╔╝██║   ██║   ██║
              ██╔══██║██║     ██║╚██╔╝██║██╔══██╗██║   ██║   ██║
              ██║  ██║╚██████╗██║ ╚═╝ ██║██████╔╝╚██████╔╝   ██║
              ╚═╝  ╚═╝ ╚═════╝╚═╝     ╚═╝╚═════╝  ╚═════╝    ╚═╝

  '"\e[0m"

  # http://www.glassgiant.com/ascii/
  echo -e "\e[94m" '
......................................MMN ......................................
....................................MMMMMMM ....................................
.......................... ........MMMMMMMMM....................................
................. ... .........  MMMMMMMMMMMMM ............... ..... .. .  .. ..
................................MMMMMMMMMMMMMMM,..................... ..... .. .
..............................MMMMMMMMMMMMMMMMMMM ..............................
............................,MMMMMMMMMMMMMMMMMMMMM$.............................
...........................MMMMMMMMMMMMMMMMMMMMMMMMM............................
.........................MMMMMMMMMMMMMMMMMMMMMMMMMMMMM .........................
........................MMMMMMMMMMMM$.  ..IMMMMMMMMMMMM.........................
......................MMMMMMMM,................. MMMMMMMM ......................
....   ..............MMMMMM .....DMMMMMMMMMMMM......MMMMMM,.....................
...................MMMMMM ...~MMMMMMMMMMMMMMMMMMMO... MMMMMM ...................
..................MMMMM... MMMMMMMMMMMMMMMMMMMMMMMMM....MMMMM$..................
............... MMMMM... MMMMMMMMMMMMMMMMMMMMMMMMMMMMM....MMMMM.................
..............7MMMMM...MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM...MMMMMM ..............
.............MMMMMM.. MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM...MMMMMM. ............
.....  ... MMMMMMM ..MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM . MMMMMMM ...........
..... ....MMMMMMM...MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM...MMMMMMM, .........
.....   MMMMMMMMM..MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM..7MMMMMMMM ........
..... ,MMMMMMMMM...MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM ..MMMMMMMMM$ ......
.... MMMMMMMMMMM..MMMM: .. MMMMMMMMM....8MO::MM...$MMN...MMMM..DMMMMMMMMMM. ....
...$MMMMMMMMMMM...MMM.. .....MMMM.......NMM................MM...MMMMMMMMMMMM ...
. MMMMMMMMMMMMM.. MMMMMMMM....MM....MMMMMMM...MMM....MMD...MM:..MMMMMMMMMMMMM, .
MMMMMMMMMMMMMMM.. MMMO........MM...MMMMMMMM...MMM ...MMM...MMM..MMMMMMMMMMMMMMM.
MMMMMMMMMMMMMMM.. MM ...MM,...MM...MMMMMMMM...MMM ...MMM...MMM..MMMMMMMMMMMMMMM
. MMMMMMMMMMMMM.. MM...MMM....MM....MMMMMMM...MMM ...MMM...MM...MMMMMMMMMMMMM...
...:MMMMMMMMMMM...MM....  ....MMM.......?MM...MMM ...MMM...MM...MMMMMMMMMMMN....
.... MMMMMMMMMMM..MMMM ..MM~==MMMMMN....MMM===MMM:==+MMM===MM..NMMMMMMMMMM......
.......MMMMMMMMM...MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM...MMMMMMMMM=.......
........MMMMMMMMM..MMMMMMMMMM.MMM..M....NMM..MMM..MMMMMMMMMM..OMMMMMMMM.........
..... ... MMMMMMM...MMMMMMMMM.MMM. M. MM.NM..8M.$.MMMMMMMMM...MMMMMMM...........
...........MMMMMMM ..MMMMMMMM.MMM. M..M. M$.I M M.MMMMMMMM.. MMMMMMM............
.............MMMMMM...MMMMMMM.MMM..M..MMMM..M..~M.MMMMMMM ..MMMMMM..............
..............,MMMMM...DMMMMM,....MM..MMMM..M..MM.MMMMMM...MMMMM8.. ............
.... ...........MMMMM... MMMMMMMMMMMMMMMMMMMMMMMMMMMMM,...MMMMM ................
..................MMMMM... MMMMMMMMMMMMMMMMMMMMMMMMM....MMMMM~..................
...................MMMMMM ....MMMMMMMMMMMMMMMMMMM~... MMMMMM....................
........ ........... MMMMMM .... +MMMMMMMMMMMZ......MMMMMM .....................
.....   ..............MMMMMMMM$................ :MMMMMMMN.......................
........................MMMMMMMMMMMMM=. .:NMMMMMMMMMMMM.........................
.........................DMMMMMMMMMMMMMMMMMMMMMMMMMMMM..........................
...........................MMMMMMMMMMMMMMMMMMMMMMMMM............................
.............................MMMMMMMMMMMMMMMMMMMMM=.............................
..............................MMMMMMMMMMMMMMMMMMM...............................
....  ..........................MMMMMMMMMMMMMMM.................................
....  ...........................MMMMMMMMMMMMM..................................
 ... .. ...........................MMMMMMMMM....................................
.... . .............................8MMMMMM.....................................
......................................MMM.......................................
 ......................................,........................................
                                                                 GlassGiant.com
 '"\e[0m"


  echo -e "\e[92m" '
 USAGE:
     ./run_res.sh -h | --help
     ./run_res.sh <opt>

     opt:
         -r | --run       Build and run bot inside container
         -s | --stop      Stop container bot and --clean
         -c | --clean     Remove image and container
         -l | --log     See running container log
'

 exit 0
}



function _pick_log() {
  _getAlias
  docker cp ${ALIAS}:/logger.log ${DIR}
	docker logs -f ${ALIAS} &>> ${DIR}/container.log
}

function _setAlias(){
  export ALIAS=${1}
}

function _getAlias(){
  export ALIAS=${ALIAS}
}



function _func_build(){
  _getAlias
  docker build \
    --quiet \
    --file Dockerfile \
    --tag ${ALIAS} \
    ${DIR} > /dev/null 2>&1
  echo "${NAME}: Build ${ALIAS}"
}

function _func_run(){
  _getAlias
  _func_stop
  _func_build
  docker run \
    --detach \
  	--name ${ALIAS} \
  	--log-driver=json-file \
  	${ALIAS} > /dev/null 2>&1
  echo "${NAME}: Running ${ALIAS} ..."
}

function _func_clean() {
  _getAlias
  docker rm ${ALIAS} > /dev/null 2>&1
  docker rmi ${ALIAS} > /dev/null 2>&1
  echo "${NAME}: Clean ${ALIAS}"
}


function _func_stop(){
  _getAlias
  docker stop ${ALIAS} > /dev/null 2>&1
  echo "${NAME}: Stop ${ALIAS}"
  _pick_log
  _func_clean
}

function log() {
  _getAlias
  docker logs -f ${ALIAS}
}



function main() {

  argc=$#
  argv=( "$@" )


  # check arguments
  if [[ $# -eq 0 ]]; then
  	print_usage

  	exit 0
  fi


  TEMP=$(getopt -o rsclh --long run,stop,clean,log,h,help, -- "${argv[@]}")
  ex=$?
  [ ${ex} -eq 2 ] && echo "Parameter is not correct." && exit 1
  [ ${ex} -ne 0 ] && echo "Error in getopt" && exit 1
  eval set -- "${TEMP}"
  while true ; do
    case ${1} in
      -a|--alias)
        _setAlias ${1}
        shift 2 ;;
      -r|--run)
        _func_run
        shift 1 ;;
      -s|--stop)
        _func_stop
        shift 1 ;;
      -c|--clean)
        _func_clean
        shift 1 ;;
      -h|-help|--h|--help )
        print_help ; exit 0 ;;
      --) shift ;  break ;;
      *) print_usage;  exit 1 ;;
    esac
  done

}


#
# <- FUNCTIONS
#



#
# -> MAIN
#

main "$@"
exit $?

#
# <- MAIN
#
