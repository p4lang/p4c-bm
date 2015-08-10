./test > test.output 2>/dev/null
DIFF=$(diff test.output test.output.ref) 
if [ "$DIFF" != "" ] 
then
    echo "FAIL!"
    exit 1
else
    echo "PASS!"
    exit 0
fi
