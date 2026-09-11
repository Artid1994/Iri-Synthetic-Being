#!/usr/bin/env bash

# NAME is the language code, e..g, eng for English
name=$NAME
export language=$name

wget -q https://huggingface.co/facebook/mms-tts/resolve/main/models/$name/G_100000.pth
wget -q https://huggingface.co/facebook/mms-tts/resolve/main/models/$name/config.json
wget -q https://huggingface.co/facebook/mms-tts/resolve/main/models/$name/vocab.txt

cat >README.md <<EOF
# Introduction

This model is converted from
https://huggingface.co/facebook/mms-tts/resolve/main/models/$name/G_100000.pth

Please see
https://huggingface.co/facebook/mms-tts/tree/main/models/$name
for more details.
EOF

pip install -qq onnx scipy Cython
pip install -qq torch==1.13.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

git clone https://huggingface.co/spaces/mms-meta/MMS
export PYTHONPATH=$PWD/MMS:$PYTHONPATH
export PYTHONPATH=$PWD/MMS/vits:$PYTHONPATH

pushd MMS/vits/monotonic_align

python3 setup.py build

ls -lh build/
ls -lh build/lib*/
ls -lh build/lib*/*/

cp build/lib*/vits/monotonic_align/core*.so .

sed -i.bak s/.monotonic_align.core/.core/g ./__init__.py
popd

./vits-mms.py
