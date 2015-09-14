====================
smart_option_pricing
====================


.. image:: https://badgen.net/github/checks/tunnckoCore/opensource
        :target: https://badgen.net/github/checks/tunnckoCore/opensource
.. image:: https://camo.githubusercontent.com/e15a935f2751eef0e60660dbf1186b2a27a3cc996b423872ec5249a70a97bfe7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f646570656e64656e636965732d6f75742532306f66253230646174652d6f72616e6765

.. image:: https://img.shields.io/badge/version-2.3-f39f37
        
.. image:: https://img.shields.io/badge/RASPBERRY%20PI-C51A4A.svg?&style=for-the-badge&logo=raspberry%20pi&logoColor=white



## Smart pricing European options on stocks using Machine Learning

Many financial engineering models have tried to relax the Black-Scholes model and improve the empirical results. However, although these models have proved to be more efficient in terms of valuation, they are much more computationally costly. 
Therefore, in order to efficiently price financial derivatives in a way that is both fast and accurate, another approach based on data-driven models have been developed.
In this library we have a trained model using XGBoost trained using some open source data mostly which follows European options. But feel free to modify for American options.
This lib uses a auth model to prevent unwanted pull of traing dataset.


* Free software: BSD license
* Documentation: https://smart-option-pricing.readthedocs.io.


Features
--------
options pricing library leveraging Black-Scholes with parameter tunning using ML Models.
