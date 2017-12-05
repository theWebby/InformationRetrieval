#!/usr/bin/env bash

DIR="$(pwd)/results"
mkdir -p $DIR

#cd ./Document_Retrieval_Assignment_Files

printf "Running ir_engine.py"
python ir_engine.py -w binary -o ./results/binary.txt && printf "." || exit 1
python ir_engine.py -w binary -o ./results/binary_s.txt -s && printf "." || exit 1
python ir_engine.py -w binary -o ./results/binary_p.txt -p && printf "." || exit 1
python ir_engine.py -w binary -o ./results/binary_sp.txt -sp && printf "." || exit 1
python ir_engine.py -w tf -o ./results/tf.txt && printf "." || exit 1
python ir_engine.py -w tf -o ./results/tf_s.txt -s && printf "." || exit 1
python ir_engine.py -w tf -o ./results/tf_p.txt -p && printf "." || exit 1
python ir_engine.py -w tf -o ./results/tf_sp.txt -sp && printf "." || exit 1
python ir_engine.py -w tfidf -o ./results/tfidf.txt && printf "." || exit 1
python ir_engine.py -w tfidf -o ./results/tfidf_s.txt -s && printf "." || exit 1
python ir_engine.py -w tfidf -o ./results/tfidf_p.txt -p && printf "." || exit 1
python ir_engine.py -w tfidf -o ./results/tfidf_sp.txt -sp && printf "." || exit 1
printf " done\n"


printf "Running ir_eval.py"

FILE="./results/results.csv"
printf "#,weighting,preprocessing,queries,docs_retrieved,docs_relevant,docs_relevant_retrieved,precision,recall,fmeasure\n" > $FILE

printf "1 binary none " >> $FILE
python eval_ir.py -f cacm_gold_std.txt ./results/binary.txt >> $FILE 2>&1 && printf "." || exit 1
printf "2 binary stoplist " >> $FILE
python eval_ir.py -f cacm_gold_std.txt ./results/binary_s.txt >> $FILE 2>&1 && printf "." || exit 1
printf "3 binary stemming " >> $FILE
python eval_ir.py -f cacm_gold_std.txt ./results/binary_p.txt >> $FILE 2>&1 && printf "." || exit 1
printf "4 binary stemmingstoplist " >> $FILE
python eval_ir.py -f cacm_gold_std.txt ./results/binary_sp.txt >> $FILE 2>&1 && printf "." || exit 1

printf "5 tf none " >> $FILE
python eval_ir.py -f cacm_gold_std.txt ./results/tf.txt >> $FILE 2>&1 && printf "." || exit 1
printf "6 tf stoplist " >> $FILE
python eval_ir.py -f cacm_gold_std.txt ./results/tf_s.txt >> $FILE 2>&1 && printf "." || exit 1
printf "7 tf stemming " >> $FILE
python eval_ir.py -f cacm_gold_std.txt ./results/tf_p.txt >> $FILE 2>&1 && printf "." || exit 1
printf "8 tf stemmingstoplist " >> $FILE
python eval_ir.py -f cacm_gold_std.txt ./results/tf_sp.txt >> $FILE 2>&1 && printf "." || exit 1

printf "9 tfidf none " >> $FILE
python eval_ir.py -f cacm_gold_std.txt ./results/tfidf.txt >> $FILE 2>&1 && printf "." || exit 1
printf "10 tfidf stoplist " >> $FILE
python eval_ir.py -f cacm_gold_std.txt ./results/tfidf_s.txt >> $FILE 2>&1 && printf "." || exit 1
printf "11 tfidf stemming " >> $FILE
python eval_ir.py -f cacm_gold_std.txt ./results/tfidf_p.txt >> $FILE 2>&1 && printf "." || exit 1
printf "12 tfidf stemmingstoplist " >> $FILE
python eval_ir.py -f cacm_gold_std.txt ./results/tfidf_sp.txt >> $FILE 2>&1 && printf "." || exit 1
printf " done\n"

sed -i 's/ /,/g' $FILE
sed -i 's/stemmingstoplist/stemming \& stoplist/g' $FILE

echo "See '$DIR' for output"
