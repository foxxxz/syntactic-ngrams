def build(graph, n=2, feature='all', stopwords=[]):
    root = graph.root # this code is suitable for nltk.parse.dependencygraph.DependencyGraph
    if n < 2:
        print("'n' should be more than equal to 2")
        return False

    res = []
    queue = [root] # queue for heads

    def dfs(root, graph, ngram=[], n=n, step=0): # recursive dfs search
        ngram = [] if ngram == [] else ngram
        if root['word'] not in stopwords: # check stopwords
            ngram.append(root)
        else:
            step -= 1
        if step == (n - 1): # build ngrams at the end node
            if feature == 'all':
                res.append(ngram.copy())
            else:
                res.append((x[feature] for x in ngram.copy()))
        else:
            words = []
            for x in graph.get_by_address(root['address'])['deps'].values():
                if x != []:
                    words += x
            words = [graph.get_by_address(x) for x in words]
            for node in words:
                dfs(node, graph, ngram, n=n, step=step+1)
                if (ngram != []) & (node['word'] not in stopwords): # check stopwords
                    ngram.pop()

    while queue:
        head = queue.pop(0) # initialize root of dfs search
        dependent_words = []
        for x in head['deps'].values():
            if x != []:
                dependent_words += x
        dependent_words = [graph.get_by_address(x) for x in dependent_words]
        queue += dependent_words
        dfs(head, graph)
    return res