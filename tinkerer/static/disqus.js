/* Enables comments powered by Disqus */

/* Call to create thread on the page */
function disqus_thread()
{
    var dsq = document.createElement('script');
    dsq.type = 'text/javascript'; dsq.async = true;
    dsq.src = 'https://' + disqus_shortname + '.disqus.com/embed.js';
    (document.getElementsByTagName('head')[0] ||
    document.getElementsByTagName('body')[0]).appendChild(dsq);
};

/* Call to enable comment-count retrieval */
function disqus_count()
{
    var s = document.createElement('script'); s.async = true;
    s.type = 'text/javascript';
    s.src = 'https://' + disqus_shortname + '.disqus.com/count.js';
    (document.getElementsByTagName('HEAD')[0] || document.getElementsByTagName('BODY')[0]).appendChild(s);
}
