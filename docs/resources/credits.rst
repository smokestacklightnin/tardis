.. _tardiscredits:

******************************
Credits & Publication Policies
******************************

|DOI_BADGE|

We provide TARDIS as a free, open-source tool. If you are using it, please
adhere to a few policies and acknowledge the TARDIS Team.

Publication Policies
====================

If you use this code for any publications or presentations please acknowledge
it.  Please cite `Kerzendorf & Sim 2014
<http://adsabs.harvard.edu/abs/2014MNRAS.440..387K>`_  in the text and add the
following paragraph to the Acknowledgement section:

.. parsed-literal::

    This research made use of \\textsc{tardis}, a community-developed software package for spectral
    synthesis in supernovae \\citep{2014MNRAS.440..387K, |CITATION|}. The
    development of \\textsc{tardis} received support from GitHub, the Google Summer of Code
    initiative, and from ESA's Summer of Code in Space program. \\textsc{tardis} is a fiscally
    sponsored project of NumFOCUS. \\textsc{tardis} makes extensive use of Astropy and Pyne.

If you use any of the full relativity treatments or use TARDIS for modelling
Type II supernovae, also add `Spectral modeling of type II supernovae. I. Dilution factors <https://ui.adsabs.harvard.edu/abs/2019A%26A...621A..29V>`_
to the Acknowledgement.

.. parsed-literal::

    \citep{2019A&A...621A..29V}

The following BibTeX entries are needed for the references:

.. code-block:: bibtex

    @ARTICLE{2014MNRAS.440..387K,
           author = {{Kerzendorf}, W.~E. and {Sim}, S.~A.},
            title = "{A spectral synthesis code for rapid modelling of supernovae}",
          journal = {\mnras},
    archivePrefix = "arXiv",
           eprint = {1401.5469},
     primaryClass = "astro-ph.SR",
         keywords = {radiative transfer, methods: numerical, supernovae: general},
             year = 2014,
            month = may,
           volume = 440,
            pages = {387-404},
              doi = {10.1093/mnras/stu055},
           adsurl = {http://adsabs.harvard.edu/abs/2014MNRAS.440..387K},
          adsnote = {Provided by the SAO/NASA Astrophysics Data System}
    }

.. code-block:: bibtex

    @ARTICLE{2019A&A...621A..29V,
           author = {{Vogl}, C. and {Sim}, S.~A. and {Noebauer}, U.~M. and {Kerzendorf}, W.~E. and {Hillebrandt}, W.},
            title = "{Spectral modeling of type II supernovae. I. Dilution factors}",
          journal = {\aap},
         keywords = {radiative transfer, methods: numerical, stars: distances, supernovae: general, supernovae: individual: SN1999em, Astrophysics - High Energy Astrophysical Phenomena, Astrophysics - Solar and Stellar Astrophysics},
             year = "2019",
            month = "Jan",
           volume = {621},
              eid = {A29},
            pages = {A29},
              doi = {10.1051/0004-6361/201833701},
    archivePrefix = {arXiv},
           eprint = {1811.02543},
     primaryClass = {astro-ph.HE},
           adsurl = {https://ui.adsabs.harvard.edu/abs/2019A&A...621A..29V},
          adsnote = {Provided by the SAO/NASA Astrophysics Data System}
    }

.. |CITATION| replace:: kerzendorf_wolfgang_2023_8196246

.. |DOI_BADGE| image:: https://img.shields.io/badge/DOI-10.5281/zenodo.8196246-blue
                 :target: https://doi.org/10.5281/zenodo.8196246

.. code-block:: bibtex

    @software{kerzendorf_wolfgang_2023_8196246,
      author       = {Kerzendorf, Wolfgang and
                      Sim, Stuart and
                      Vogl, Christian and
                      Williamson, Marc and
                      Pássaro, Ezequiel and
                      Flörs, Andreas and
                      Camacho, Yssa and
                      Jančauskas, Vytautas and
                      Harpole, Alice and
                      Nöbauer, Ulrich and
                      Lietzau, Stefan and
                      Mishin, Mikhail and
                      Tsamis, Fotis and
                      Boyle, Aoife and
                      Shingles, Luke and
                      Gupta, Vaibhav and
                      Desai, Karan and
                      Klauser, Michael and
                      Beaujean, Frederik and
                      Suban-Loewen, Adam and
                      Heringer, Epson and
                      Barna, Barnabás and
                      Gautam, Gaurav and
                      Fullard, Andrew and
                      Smith, Isaac and
                      Cawley, Kevin and
                      Singhal, Jaladh and
                      Arya, Atharva and
                      Sondhi, Dhruv and
                      Barbosa, Talytha and
                      O'Brien, Jack and
                      Yu, Jenny and
                      Patel, Maryam and
                      Varanasi, Kaushik and
                      Gillanders, James and
                      Rathi, Shikha and
                      Chitchyan, Sona and
                      Savel, Arjun and
                      Reinecke, Martin and
                      Eweis, Youssef and
                      Bylund, Tomas and
                      Black, William and
                      Bentil, Laud and
                      Eguren, Jordi and
                      Bartnik, Matthew and
                      Alam, Arib and
                      Varma Buddaraju, Rohith and
                      Kumar, Ansh and
                      Magee, Mark and
                      Livneh, Ran and
                      Shields, Joshua and
                      Kambham, Satwik and
                      Rajagopalan, Srinath and
                      Mishra, Sashank and
                      Reichenbach, John and
                      Daksh, Ayushi and
                      Singh, Shreyas and
                      Floers, Andreas and
                      Jain, Rinkle and
                      Actions, GitHub and
                      Singh, Sourav and
                      Brar, Antreev and
                      Holas, Alexander and
                      Bhakar, Jayant and
                      Chaumal, Aarya and
                      Sofiatti, Caroline and
                      Kowalski, Nathan and
                      Talegaonkar, Chinmay and
                      Selsing, Jonatan and
                      Kumar, Aman and
                      Patidar, Abhishek and
                      Venkat, Shashank and
                      Sarafina, Nance and
                      Sharma, Sampark and
                      Patel, Pratik and
                      Singh Rathore, Parikshit and
                      Patra, Nilesh and
                      Lu, Jing and
                      Zaheer, Musabbiha and
                      Sandler, Morgan and
                      Martinez, Laureano and
                      Yap, Kevin and
                      Gupta, Suyash and
                      Prasad, Shilpi and
                      Dasgupta, Debajyoti and
                      Lemoine, Thom and
                      Wahi, Ujjwal and
                      Aggarwal, Yash and
                      Matsumura, Yuki and
                      Gupta, Harshul and
                      Volodin, Dmitry and
                      PATIDAR, ABHISHEK and
                      Truong, Le and
                      Kumar, Atul and
                      Kharkar, Atharwa and
                      Kolliboyina, Chaitanya and
                      Nayak U, Ashwin},
      title        = {tardis-sn/tardis: TARDIS v2023.07.30},
      month        = jul,
      year         = 2023,
      publisher    = {Zenodo},
      version      = {release-2023.07.30},
      doi          = {10.5281/zenodo.8196246},
      url          = {https://doi.org/10.5281/zenodo.8196246}
    }

