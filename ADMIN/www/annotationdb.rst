.. _sec-annotationdb:

===================
Annotation Database
===================

This database contains a curated collection of variant annotations in Hail-friendly format. The data lives here_ in a publically-accessible 
storage bucket on the Google Cloud Platform.

.. _here: https://console.cloud.google.com/storage/browser/hail-annotation/?project=broad-ctsa

To incorporate these annotations in your own Hail analysis pipeline, select which annotations you would like to query from the options below and 
then copy-and-paste the Hail code generated into your own analysis script.
 
-------------

Query Builder
-------------
      
.. raw:: html      

      <div class="panel-group">
         <div class="panel panel-default">
            <div class="panel-heading query clearfix">
               <a class="pull-left" role="button" data-toggle="collapse" href="#hail-code">
                  <span class="text-expand">Database Query</span>
               </a>
               <div class="btn-group pull-right">
                  <a class="btn btn-default btn-sm" data-clipboard-target="#hail-copy" id="hail-copy-btn">Copy to clipboard</a>
               </div>
            </div>
            <div class="panel-collapse collapse in" id="hail-code">
               <div class="panel-body hail-code">
                  <span class="hail-code query placeholder" id="hail-copy"></span>
               </div>
            </div>
         </div>
         <div class="panel panel-default">
            <div class="panel-heading query clearfix">
               <a class="pull-left" role="button" data-toggle="collapse" href="#annotations">
                  <span class="text-expand">Annotations</span>
               </a>
               <div class="btn-group pull-right">
                  <a class="btn btn-default btn-sm" id="annotations-clear">Clear selections</a>
               </div>
            </div>
            <div class="panel-collapse collapse in" id="annotations">
               <div class="panel-body annotations">
                  <div id="tree"></div>
               </div>
            </div>
         </div>
      </div>

-------------

Documentation
-------------

These annotations have been collected from a variety of publications and their accompanying datasets (usually text files). Links to the relevant
publications and raw data downloads are included where applicable.
   
.. raw:: html

   <div class="panel-group" id="panel-docs">
   </div>
