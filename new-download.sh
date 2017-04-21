#!/bin/bash

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
  rm -f ${dst_file};
  curl -o $dst_file $msn_src;

  #
  # Parse JSON to csv; output:
  #   1       | 2             | 3   | 4
  #   prb ID  | CHAOS string  | RTT | RCODE
  parsed_file="json_result/${l}-${init_time}.csv";
  rm -f ${parsed_file};
  python json-parser/parser.py ${dst_file} ${parsed_file};

  #
  # Validate strings for the root server and print airport code for the site of instance hit; output:
  #   2       | 2             | 3   | 4
  #   prb ID  | CHAOS string  | RTT | RCODE
  rm -f ${clean_file};
  clean_file="json_result/${l}-${init_time}-clean.csv";
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
  stats_file_time="stats_result/${l}-${init_time}.csv";
  stats_file_all="stats_result/${l}.csv";

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
  out_path="stats_result/${l}";
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

        #
        ## NUMBER OF QUERIES (3rd column) STILL HAS TO BE COMPUTED

        printf "%s,%d,NA,%d,%.04f,%.04f,%.04f,%.04f\n",
                 TS, _probes,site_hit[s],
                 _25_rtt, _50_rtt, _75_rtt, _90_rtt >> output_file;

      }

    }' TS=${init_time} OUT_PATH=${out_path} ${clean_file};


  rm -f ${dst_file} ${parsed_file};

done;







