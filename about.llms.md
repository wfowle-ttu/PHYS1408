# About

This site is my documentation site for my notes taken during PHYS1408. Typically, I will either take notes by hand and then transcribe them into this site or I will just write them directly on a document.

I will use this sidebar strategy for loading contents into the site:

### Auto Generation

Above we describe how to explicitly populate the contents of your sidebar with navigation items. You can also automatically generate sidebar navigation from the filesystem. The most straightforward way to do this is to specify the contents option as follows:

sidebar: contents: auto

Using contents: auto at the root level will result in all documents in your website being included within the navigation (save for the home page which can be navigated to via the title link). Navigation is constructed using the following rules:

    Navigation item titles will be read from the title field of documents.

    Sub-directories will create sections and will be automatically titled based on the directory name (including adding capitalization and substituting spaces for dashes and underscores). Use an index.qmd in the directory to provide an explicit title if you don’t like the automatic one.

    Order is alphabetical (by filename) unless a numeric order field is provided in document metadata.

Automatic navigation automatically includes items in sub-directories. If you prefer not to do this, use an explicit /\* to indicate only the documents in the root directory:

Ergo notes and their section layout are determined by Quarto’s automatic layout from the contents being set to auto.
