Database
========

The Sphinx build exports the CSV tables from ``docs/content/tables/`` to a SQLite database at ``docs/_build/html/database/boolean_wiki.db``.

The Datasette Lite documentation is located in ``datasettelite-docs.md``.

Open the generated SQLite database in Datasette Lite:

For local testing, run ``./run_wiki.sh`` from the repository root so Datasette Lite can load ``docs/_build/html/database/boolean_wiki.db`` with the required CORS headers.

Database Terminal
-----------------

.. raw:: html

   <p>
     <a id="sqlite-database-link" href="../../database/boolean_wiki.db">Open boolean_wiki.db directly</a>
     <br>
     <a id="datasette-lite-link" href="https://lite.datasette.io/">Open boolean_wiki.db in Datasette Lite</a>
   </p>
   <div style="border: 1px solid #ccc; border-radius: 8px; overflow: hidden;">
       <iframe
           id="datasette-iframe"
           src="about:blank"
           width="100%"
           height="600"
           frameborder="0">
       </iframe>
   </div>

   <script>
   (function () {
     var iframe = document.getElementById("datasette-iframe");
     var databaseLink = document.getElementById("sqlite-database-link");
     var datasetteLink = document.getElementById("datasette-lite-link");
     if (!iframe) return;
     if (!databaseLink) return;

     var databaseUrl = new URL(databaseLink.getAttribute("href"), window.location.href).href;
     var datasetteUrl = "https://lite.datasette.io/?url=" + encodeURIComponent(databaseUrl);
     if (datasetteLink) {
       datasetteLink.href = datasetteUrl;
     }
     iframe.src = datasetteUrl + "&embed=1";
   }());
   </script>
