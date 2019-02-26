.. snpFC documentation master file, created by
   sphinx-quickstart on Mon Feb 11 16:08:30 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to documentation of snpFC
=================================

Introduction
^^^^^^^^^^^^

snpFC - a python tool for filtering and comparing SNPs from two or multiple VCF files.

How can I get it
^^^^^^^^^^^^^^^^

At the moment, latest snpFC tool can be obtained from github repo `link <https://github.com/TSL-RamKrishna/snpminer_webtool>`_ . Just clone the repository or download as a compressed file.

I have a target to upload snpFC to python repository enabling to install using pip command.

Pre-requisites
^^^^^^^^^^^^^^

Assuming you have python3 already, install pyVCF ::
        
        pip install pyvcf

Quick Start
^^^^^^^^^^^

If you don't have patience, here is how to run snpFC ::
        
        python scripts/filter_and_comparesnps.py --vcf testfiles/test1.vcf testfiles/test2.vcf --filter --compare --show --frequency 70 --pvalue 0.05 --genotype heterozygous --quality 10 --rawreaddepth 5 --qualityreaddepth 5 --depthreference 5 --depthvariant 5 --outdir ./testfiles

The above command will output as following ::

        Common and Unique SNPS in vcf File :  testfiles/test1.vcf
        tig00000003 775 A G common
        tig00000003 776 T C common
        tig00000003 836 G C unique
        tig00000004 1166 G A common
        tig00000004 1190 G A unique
        Common and Unique SNPS in vcf File :  testfiles/test2.vcf
        tig00000003 775 A G common
        tig00000003 776 T C common
        tig00000003 836 G T unique
        tig00000004 1166 G A common
        tig00000004 1190 G A,C unique
        The outputs are saved in these files : /home/shrestha/Sites/test1_snpanalysis.txt /home/shrestha/Sites/test2_snpanalysis.txt



Options
^^^^^^^ 

Available options::

        --vcf                   space separated two or more vcf files
        --filter                filter snps
        --compare               compare snps between vcf files
        --frequency             frequency threshold value to filter (default: 70)
        --pvalue                pvalue threshold value to filter ( default: 0.05)
        --genotype              genotype to filter (default: heterozygous)
        --quality               genotype quality threshold to filter (default: 10)
        --rawreaddepth          raw read depth threshold to filter (default: 5)
        --qualityreaddepth      quality read depth threshold to filter (default:5)
        --depthreference        depth in reference threshold to filter (default:5)
        --depthvariant          depth in variant threshold to filter (default:5)
        --show                  show the compared snps on screen 
        --outdir                output directory

To check the options::
        
        python scripts/filter_and_comparesnps.py --help



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

   contributions
   
   help


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
