#!/bin/bash
#
# Usage:
#   ./parse-json.sh <START timestamp> <STOP timestamp> <interval> <measurement ID>
#
# Notes:
#   - START and STOP timestamps are epoch (GMT)
#   - interval is the bin size for analysis (in seconds)
#   - measurement ID has to be a CHAOS measurement produced by RIPE Atlas
#
# YOU have to create the following folder structure:
#   - atlas_input: to temporarily store JSON files downloaded from RIPE Atlas
#   - json_result: to store processed csv files
#   - stats_result: to store general letter (service) results
#   - stats_result/sites: to store individual sites (servers) results
#


path_atlas_json="atlas_input/";
path_json_result="json_result/";

if [ $# -ne 4 ]; then
  echo "ERROR! number of arguments is not correct. Usage:";
  echo "    #1: start time of measurement";
  echo "    #2: stop time of measurement";
  echo "    #3: bit size in seconds";
  echo "    #4: measurement ID";
  exit;
fi;

# This are the times specified for the interval to retrieve CHAOS results
init_time=$1;
stop_time=$2;
# Bin size for measurments
bin_size=$3;
# This is the measurement ID of CHAOS queries
msn_id=$4;

error=`echo "$init_time $stop_time" | awk '{if($1>$2) print "1"; else print "0";}'`;
if [ $error -eq 1 ]; then
  echo "ERROR! start time should be smaller than stop time";
  exit;
fi;

let cur_stop_time=$init_time+$bin_size;
let cur_init_time=$init_time;

while [ $cur_stop_time -le $stop_time ]; do

  echo "*** current period from $cur_init_time to $cur_stop_time";

  #
  # Download JSON
  msn_src="https://atlas.ripe.net/api/v2/measurements/${msn_id}/results?start=${cur_init_time}&stop=${cur_stop_time}&format=json";
  dst_file="atlas_input/letter-${cur_init_time}.json";
  rm -f ${dst_file};
  curl -o $dst_file $msn_src;

  let cur_init_time=$cur_stop_time;
  let cur_stop_time+=$bin_size;

  #
  # Parse JSON to csv; output:
  #   1       | 2             | 3   | 4
  #   prb ID  | CHAOS string  | RTT | RCODE
  parsed_file="json_result/letter-${cur_init_time}.csv";
  rm -f ${parsed_file};
  python json-parser/parser.py ${dst_file} ${parsed_file};

  #
  # Validate strings for the root server and print airport code for the site of instance hit; output:
  #   2       | 2             | 3   | 4
  #   prb ID  | CHAOS string  | RTT | RCODE
  rm -f ${clean_file};
  clean_file="json_result/letter-${cur_init_time}-clean.csv";
  awk '
    {
      if (NF > 1) {
        if (index($2, ".k.ripe.net") != 0) {
          if (index($2, "[u") != 0)
            server_name = substr($2,4,length($2)-5);
          else
            server_name = $2;

          if (substr(server_name, 1, 1) == "k")
            print $1, substr(server_name,4,length($2)-3), $3, $4;
          else
            print $1, substr(server_name,5,length($2)-4), $3, $4;
        }
      }
    }' ${parsed_file} > ${clean_file};

  #
  # calculate per-letter statistics
  stats_file_time="stats_result/letter-${cur_init_time}.csv";
  stats_file_all="stats_result/letter.csv";

  _stat_number_probes=`cut -f 1 -d ' ' ${clean_file} | sort -n | uniq | wc -l | awk '{print $1;}'`;
  _stat_number_sites=`cut -f 2 -d ' ' ${clean_file} | sort | uniq | wc -l | awk '{print $1;}'`;
  _stat_number_replies=`awk 'BEGIN{tot=0;}{if ($4==0) tot++;}END{print tot;}' ${clean_file}`;
  _stat_number_queries=`wc -l ${clean_file} | awk '{print $1;}'`;

  _stat_rtt=`cut -f 3 -d ' ' ${clean_file} |\
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
    echo "timestamp,nProbes,nSites,nQueries,nResponses,q25RTT,q50RTT,q75RTT,q90RTT" >> $stats_file_all;
  fi;
  echo "$init_time,$_stat_number_probes,$_stat_number_sites,$_stat_number_queries,$_stat_number_replies,$_stat_rtt" >> $stats_file_all;


  #
  # calculate per-site statistics
  out_path="stats_result/sites";
  gawk '
    {
      site_hit[$2]++;
      site_rtt[$2][site_hit[$2]] = $3;
      site_probes[$2][$1]++;
    }
    END {
      for (s in site_hit) {
        asort(site_rtt[s],site_rtt_sorted);
        
        i = length(site_rtt_sorted);
        if (i%2 == 0)
          _50_rtt = (site_rtt_sorted[i/2] + site_rtt_sorted[(i/2)+1])/2;
        else
          _50_rtt = site_rtt_sorted[int(i/2)+1];

        _25_rtt = site_rtt_sorted[int(i*0.25)];
        _75_rtt = site_rtt_sorted[int(i*0.75)];
        _90_rtt = site_rtt_sorted[int(i*0.90)];

        _probes = length(site_probes[s]);

        output_file = OUT_PATH"/"s;

        if (system("test -f " output_file) != 0)
          printf "timestamp,nProbes,nQueries,nResponses,q25RTT,q50RTT,q75RTT,q90RTT\n" > output_file;

        ## TODO: NUMBER OF QUERIES (3rd column) STILL HAS TO BE COMPUTED ##

        printf "%s,%d,NA,%d,%.04f,%.04f,%.04f,%.04f\n",
                 TS, _probes,site_hit[s],
                 _25_rtt, _50_rtt, _75_rtt, _90_rtt >> output_file;

      }

    }' TS=${init_time} OUT_PATH=${out_path} ${clean_file};


  rm -f ${dst_file} ${parsed_file};


done;





