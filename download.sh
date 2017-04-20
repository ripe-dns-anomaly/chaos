#!/bin/bash
#
# Ricardo de Oliveira Schmidt
#   April 20, 2017
#
# Description:
#   Download JSON files from RIPE CHAOS queries and parse content.
#
# Usage:
#   ./download.sh <INIT_TIME> <STOP_TIME>
#


declare -a root_letter=( "a" "b" "c" "d" "e" "f" "g" "h" "i" "j" "k" "l" "m" );
declare -a msn_id_v4=( "10309" "10310" "10311" "10312" "10313" "10304" "10314" "10315" "10305" "10316" "10301" "10308" "10306" );

declare -a root_letter=( "k" );
declare -a msn_id_v4=( "10301" );

declare -i count_letter=-1;
declare -i skip=1;

path_atlas_json="atlas_input/";
path_json_result="json_result/";


if [ $# -ne 2 ]; then
  echo "ERROR: see usage for arguments.";
  exit;
fi;

# This are the times specified for the interval to retrieve CHAOS results
init_time=$1
stop_time=$2;


# Loop to download and process per root letter
count_letter=-1;
for l in ${root_letter}; do

  count_letter+=1;

  #
  # Download JSON
  msn_src="https://atlas.ripe.net/api/v2/measurements/${msn_id_v4[$count_letter]}/results?start=${init_time}&stop=${stop_time}&format=json";
  dst_file="atlas_input/${l}-${init_time}.json";
#  rm -f ${dst_file};
#  curl -o $dst_file $msn_src;

  #
  # Parse JSON to csv; output:
  #   1       | 2             | 3
  #   prb ID  | CHAOS string  | RTT
  parsed_file="json_result/${l}-${init_time}.csv";
  rm -f ${parsed_file};
  python parse-chaos.py ${dst_file} ${parsed_file};

  #
  # Validate strings for the root server and print airport code for the site of instance hit; output:
  #   2       | 2             | 3             | 4
  #   prb ID  | CHAOS string  | airport code  | RTT
  rm -f ${clean_file};
  clean_file="json_result/${l}-${init_time}-clean.csv";
  awk '
    {
      if (NF > 1) {
        if (index($2, ".k.ripe.net") != 0 && substr($2,1,2) == "ns" && length($2) >= 21)
          print $1, $2, substr($2,index($2,"-")+1,3), $3;
      }
    }' ${parsed_file} > ${clean_file};

  #
  # calculate per-letter statistics
  stats_file_time="stats_result/${l}-${init_time}.csv";
  stats_file_all="stats_result/${l}.csv";
  _stat_number_probes=`cut -f 1 -d ' ' ${clean_file} | sort -n | uniq | wc -l | awk '{print $1;}'`;
	_stat_number_sites=`cut -f 3 -d ' ' ${clean_file} | sort | uniq | wc -l | awk '{print $1;}'`;
	_stat_number_replies=`wc -l ${clean_file} | awk '{print $1;}'`;
  _stat_number_queries=`python count-queries.py ${dst_file}`;
	_stat_rtt=`cut -f 4 -d ' ' ${clean_file} |\
		sort -n |\
		awk '{
				_rtt[++i] = $1;
			}
			END {
				if (i%2 == 0)
					_50_rtt = (_rtt[i/2]+_rtt[(i/2)+1])/2;
				else
					_50_rtt = _rtt[int(i/2)+1];

				_25_rtt = _rtt[int(i*0.25)]; 
				_75_rtt = _rtt[int(i*0.75)]; 
				_90_rtt = _rtt[int(i*0.90)]; 

				printf "%.04f,%.04f,%.04f,%.04f", _25_rtt, _50_rtt, _75_rtt, _90_rtt;
			}'`;

  if [ ! -f $stats_file_all ]; then
  	echo "timestamp,nSites,nQueries,nResponses,q25RTT,q50RTT,q75RTT,q90RTT" >> $stats_file_all;
  fi;
	echo "$init_time,$_stat_number_probes,$_stat_number_sites,$_stat_number_queries,$_stat_number_replies,$_stat_rtt" >> $stats_file_all;


  #
  # calculate per-site statistics
#  gawk '
#    {
#      site[$3]++;
#      site_rtt[$3][length(site[$3])] = $4;
#    }
#  ' ${clean_file};






  rm -f ${dst_file};

done;







