while true; do
    a=$((1 + $RANDOM % 3))
    b=$((1 + $RANDOM % 3))
    c=$((1 + $RANDOM % 3))
    d=$((1 + $RANDOM % 3))
    curl http://127.0.0.1:5081/payload?"oof${a}=rab${b}&foo${c}=bar${d}"
done
