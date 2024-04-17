# AnnotatePDF
Search and color code the text in the PDF for better readability

# Required Python library
```
pip install PyMuPDF
```

### Run

Like many of the libraries available, the python wrappers subscribe to the same API as [sklearn.manifold.TSNE](http://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html).

You can run it as follows:

```
from tsnecuda import TSNE
X_embedded = TSNE(n_components=2, perplexity=15, learning_rate=10).fit_transform(X)
```
