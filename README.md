# Feature-Model Benchmark

Our feature model benchmark provides large, real-world feature models for empirical evaluations.

Below you will find a table with all the currently available feature models and their sources of origin.
With scripts/fmb_search.py you can search for feature models with specific characteristics in the categories
 - Domain
 - Format
 - Features
 - CTC

The search procedure is convenient and offers three choices:
 1. Search for a single category
 	1. Enter one category
	2. Press Enter
	3. Enter the search value
	4. Press Enter
	5. Resulting feature models are shown
 2. Search for multiple categories looking for an intersection of sets of feature models (comma as logical AND)
	1. Enter at least two categories and separate them by comma or ampersand
	2. Press Enter
	3. Enter the search value, separating the search values by comma or ampersand
	4. Press Enter
	5. Resulting feature models fulfilling all criteria are shown
 3. Search for multiple categories looking for a union of sets of feature models (semicolon as logical OR)
 	1. Enter at least two categories and separate them by semicolon or pipe
	2. Press Enter
	3. Enter the search value, separating the search values by semicolon or pipe
	4. Press Enter
	5. Resulting feature models fulfilling at least one of the criteria are shown

(When entering categories domain or format, the available items are printed to the console)

Special search operations (only for use in search values, not categories):
 1. Greater than: >"Number" (e.g., more than 500: >500)
 2. Less than:    <"Number" (e.g., less than 500: <500)
 3. Range:        "Number"to"Number" (e.g., between 500 and 800: 500to800 or 500-800)
 4. NOT:          -"Value" (e.g., not of domain systems software: -systems software)

Saving found feature models in an extra directory:
 - commands: fmb, create benchmark
 - if it doesn't exist, a new directory "benchmarks" is created next to "scripts" etc.
 - Feature-model files of feature models found during search are copied in a subdirectory of benchmarks

Get all available feature models:
 - commands: Nothing (i.e., just press "Enter"), all
 - To save all available feature models in a new subdirectory of benchmarks:
   1. fmb
   2. "Enter"

Additional commands:
 - help
 - exit
 - show domains
 - show formats

Examples:
 1. Find all feature models of domain automotive: 
	- *Enter* domain *and then* automotive
 2. Find feature models with domain systems software and format FeatureIDE: 
	- *Enter* domain,format *and then* systems software,FeatureIDE
	- *Enter* domain&format *and then* systems software&FeatureIDE
 3. Find all feature models of domain finance with more than 700 features: 
	- *Enter* domain,features *and then* finance,>700
	- *Enter* domain&features *and then* finance&>700
 4. Find feature models of domain business or with more than 70,000 features: 
	- *Enter* domain;features *and then* business;>70000
	- *Enter* domain|features *and then* business|>70000
 5. Find feature models of domain systems software but not format DIMACS
	- *Enter* domain,features *and then* systems software,-DIMACS
 6. Find feature models of domain business or not format DIMACS
	- *Enter* domain;format *and then* business;-DIMACS

| Name | Domain | Format | #Features | #CTC | Source |
| --- | --- | --- | --- | --- | --- |
| automotive2_4 | automotive | FeatureIDE | 18616 | 1369 | Knüppel et al. 2017 https://doi.org/10.1145/3106237.3106252 |
| automotive2_3 | automotive | FeatureIDE | 18434 | 1300 | Knüppel et al. 2017 https://doi.org/10.1145/3106237.3106252 |
| automotive2_2 | automotive | FeatureIDE | 17742 | 914  | Knüppel et al. 2017 https://doi.org/10.1145/3106237.3106252 |
| automotive2_1 | automotive | FeatureIDE | 14010 | 666  | Knüppel et al. 2017 https://doi.org/10.1145/3106237.3106252 |
| linux-2.6.33.3       | systems software | FeatureIDE | 6467 | 3545 | Knüppel et al. 2017 https://doi.org/10.1145/3106237.3106252 |
| uClinux-distribution | systems software | FeatureIDE | 1580 | 197  | Knüppel et al. 2017 https://doi.org/10.1145/3106237.3106252 |
| embtoolkit           | systems software | FeatureIDE | 1179 | 323  | Knüppel et al. 2017 https://doi.org/10.1145/3106237.3106252 |
| busybox-1.18.0       | systems software | FeatureIDE | 854  | 123  | Knüppel et al. 2017 https://doi.org/10.1145/3106237.3106252 |
| uClinux-base         | systems software | FeatureIDE | 380  | 3455 | Knüppel et al. 2017 https://doi.org/10.1145/3106237.3106252 |
| uClibc               | systems software | FeatureIDE | 313  | 56   | Knüppel et al. 2017 https://doi.org/10.1145/3106237.3106252 |
| Automotive1 | automotive | XML | 2513  | 2833 | Al-Hajjaji et al. 2019 https://doi.org/10.1007/s10270-016-0569-2 |
| FinancialServices01_2017-05-22 | finance | FeatureIDE | 557 | 1001 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| FinancialServices01_2017-09-28 | finance | FeatureIDE | 704 | 1136 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| FinancialServices01_2017-10-20 | finance | FeatureIDE | 712 | 1142 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| FinancialServices01_2017-11-20 | finance | FeatureIDE | 711 | 1148 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| FinancialServices01_2017-12-22 | finance | FeatureIDE | 716 | 1148 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| FinancialServices01_2018-01-23 | finance | FeatureIDE | 712 | 1028 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| FinancialServices01_2018-02-20 | finance | FeatureIDE | 759 | 1034 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| FinancialServices01_2018-03-26 | finance | FeatureIDE | 771 | 1080 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| FinancialServices01_2018-04-23 | finance | FeatureIDE | 774 | 1079 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| FinancialServices01_2018-05-09 | finance | FeatureIDE | 771 | 1080 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2013-11-06T06_39_45+01_00[^1] | systems software | DIMACS | 49247 | 477705 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2013-11-06T08_16_28+01_00[^1] | systems software | DIMACS | 49246 | 478610 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2013-11-17T11_31_48+01_00[^1] | systems software | DIMACS | 49255 | 478340 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2013-12-11T15_52_34+01_00[^1] | systems software | DIMACS | 49785 | 477274 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2014-01-02T15_48_22-08_00[^1] | systems software | DIMACS | 49752 | 484039 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2014-01-06T10_43_58-05_00[^1] | systems software | DIMACS | 49813 | 484444 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2014-12-19T13_22_42-08_00[^1] | systems software | DIMACS | 57461 | 559942 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2014-12-19T14_02_02-08_00[^1] | systems software | DIMACS | 57443 | 560133 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2015-01-06T11_04_29-08_00[^1] | systems software | DIMACS | 57443 | 561320 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2015-01-16T14_40_14+01_00[^1] | systems software | DIMACS | 57464 | 560616 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2015-10-21T11_22_12+02_00[^1] | systems software | DIMACS | 62633 | 616929 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2015-11-03T18_59_10-08_00[^1] | systems software | DIMACS | 62645 | 618224 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2016-01-07T14_11_32+01_00[^1] | systems software | DIMACS | 63903 | 629250 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2016-01-09T06_30_49-08_00[^1] | systems software | DIMACS | 63861 | 628683 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2016-12-18T15_45_33-08_00[^1] | systems software | DIMACS | 71547 | 713145 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2016-12-22T09_25_45-08_00[^1] | systems software | DIMACS | 71561 | 715356 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2017-01-11T13_56_49+00_00[^1] | systems software | DIMACS | 71560 | 712929 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2017-01-24T09_14_52+01_00[^1] | systems software | DIMACS | 71576 | 715425 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2017-12-22T20_13_00+01_00[^1] | systems software | DIMACS | 76407 | 763837 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2017-12-23T11_53_04-08_00[^1] | systems software | DIMACS | 76820 | 773125 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2018-01-08T11_10_40+01_00[^1] | systems software | DIMACS | 76457 | 766644 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2018-01-08T20_05_04+01_00[^1] | systems software | DIMACS | 77003 | 773998 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2018-01-12T00_14_28+01_00[^1] | systems software | DIMACS | 76453 | 766133 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| Linux-2018-01-14T09_51_25-08_00[^1] | systems software | DIMACS | 76815 | 774148 | Pett et al. 2019 https://doi.org/10.1145/3336294.3336322 |
| ERP-System[^2]     | business   | SXFM | 1653 | 59044 | Pereira et al. 2016 https://doi.org/10.1145/2993236.2993249 |
| E-Agribusiness[^2] | e-Commerce | SXFM | 2008 | 0 | Pereira et al. 2016 https://doi.org/10.1145/2993236.2993249 |
| eCos-benchmark-clafer (116 feature models)[^3] | systems software | Clafer | 1230 || Passos et al. 2011 https://doi.org/10.1145/2019136.2019139 |
| 2.6.28.6 | systems software | DIMACS | 11400 | 229794 | Saber et al. 2018 https://doi.org/10.1016/j.infsof.2017.08.010 |
| main_full[^2]  | deep learning | SXFM | 6867 | 9 | Ghamizi et al. 2019 https://doi.org/10.1145/3336294.3336306 |
| main_light[^2] | deep learning | SXFM | 3296 | 76 | Ghamizi et al. 2019 https://doi.org/10.1145/3336294.3336306 |
| 2.6.33.3-2var    | systems software | DIMACS | 62482 | 273799 | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| 2.6.32-2var      | systems software | DIMACS | 60072 | 268223 | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| freetz           | systems software | DIMACS | 31012 | 102705 | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| embtoolkit       | systems software | DIMACS | 23516 | 180511 | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| buildroot        | systems software | DIMACS | 14910 | 45603  | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| uClinux-config   | systems software | DIMACS | 11254 | 31637  | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| 2.6.28.6-icse11  | systems software | DIMACS | 6888  | 343944 | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| busybox-1.18.0   | systems software | DIMACS | 6796  | 17836  | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| uClinux          | systems software | DIMACS | 1850  | 2468   | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| fiasco           | systems software | DIMACS | 1638  | 5228   | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| freebsd-icse11   | systems software | DIMACS | 1396  | 62163  | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| phycore229x      | systems software | DIMACS | 1360  | 4026   | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| m5272c3          | systems software | DIMACS | 1323  | 3297   | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| se77x9           | systems software | DIMACS | 1319  | 49937  | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| at91sam7sek      | systems software | DIMACS | 1319  | 3963   | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| adderII          | systems software | DIMACS | 1276  | 3206   | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| olpce2294        | systems software | DIMACS | 1274  | 3881   | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| integrator_arm9  | systems software | DIMACS | 1267  | 50606  | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| pati             | systems software | DIMACS | 1248  | 3266   | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| ecos-icse11      | systems software | DIMACS | 1244  | 3146   | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| ref4955          | systems software | DIMACS | 1218  | 3099   | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| busybox_1_28_0   | systems software | DIMACS | 998   | 962    | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| axTLS            | systems software | DIMACS | 684   | 2155   | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| toybox           | systems software | DIMACS | 544   | 1020   | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| toybox_0_7_5     | systems software | DIMACS | 316   | 106    | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| uClibc-ng_1_0_29 | systems software | DIMACS | 269   | 1403   | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
| fiasco_17_10     | systems software | DIMACS | 234   | 1178   | Oh et al. 2020 Scalable Uniform Sampling for Real-World Software Product Lines (TR https://apps.cs.utexas.edu/apps/tech-reports/192690) https://github.com/jeho-oh/Smarch |
|||||||

[^1]: Information about numbers of features and cross-tree cornstraints gathered from DIMACs file (p cnf).
[^2]: Information about numbers of cross-tree constraints gathered from the SXFM files.
[^3]: Features range from 1159 to 1312, number of features here is the median given in the paper. No information about the number of cross-tree constraints is provided.