# rightload

A personal NLP and ML-based scoring proxy for RSS and Atom feeds. Run with

```
gunicorn -w 7 -t 3600 -b 127.0.0.1:5000 app:app
```

or equivalent (it's a flask app).

Entry points are `/feed/<url>` to proxy the `feed` at `url` and `/learn` to
retrain the model. It adds a feedback bar atop each entry that says "Time Well
Spent" or "Time Wasted". You need to click only if you agree. If you disagree,
it means you and the algorithm agree, and no further action is needed. It needs
some positive and negative feedback before training the model for the first
time. The title is prefixed with a score which is 100\*estimated probability of
being interesting. But in fact you could try to teach the model any binary
classification. I just use it to prioritize my reading without skimming forever.
It also adds highlighting to each sentence with intensity proportional to the
probability of "interestingness", and a superscript with the actual number. This
may be annoying to most, but it helps me understand what the algorithm is doing.
Installation is a work in progress. The hard part is installing
[Infersent](https://github.com/facebookresearch/InferSent) as a subdir of the
root of the repo. See also the [blog
entry](http://piccolboni.info/2017/11/tame-the-newsfeed-with-homemade-ai.html)
for additional information.
