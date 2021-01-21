set -eo pipefail

_stopnow() {
  test -f stopnow && echo "Stopping!" && rm stopnow && exit 0 || return 0
}

while true
do
    _stopnow
    # Below here, you put in your command you want to run:

    sudo ~/anaconda3/bin/streamlit run ~/voter-fraud-analysis/app.py
done