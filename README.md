This repo contains scripts that transform [CLIMATE-FEVER](https://www.sustainablefinance.uzh.ch/en/research/climate-fever.html)
dataset [^1] to the format that's accepted by MultiVerS models [^2] 
for [training](/format_climate_fever_for_multivers_training.py) 
and [evaluation](/format_climate_fever_for_multivers_evaluation.py)

To download example data please execute

```shell
./download-examples.sh
```

[^1]: Diggelmann, Thomas; Boyd-Graber, Jordan; Bulian, Jannis; Ciaramita, Massimiliano; 
Leippold, Markus (2020). CLIMATE-FEVER: A Dataset for Verification of Real-World Climate 
Claims. In: Tackling Climate Change with Machine Learning workshop at NeurIPS 2020, Online, 
11 December 2020 - 11 December 2020.
[^2]: Wadden, D., Lo, K., Wang, L.L., Cohan, A., Beltagy, I., & Hajishirzi, H. (2021). MultiVerS: Improving scientific claim verification with weak supervision and full-document context. NAACL-HLT.