This repo contains scripts that transform [CLIMATE-FEVER](https://www.sustainablefinance.uzh.ch/en/research/climate-fever.html)
dataset [^1] to the format that's accepted by MultiVerS models [^2] 
for [training](/format_climate_fever_for_multivers_training.py) 
and [evaluation](/format_climate_fever_for_multivers_evaluation.py)

To download example data please execute

```shell
./download-examples.sh
```

According to https://github.com/dwadden/multivers/blob/main/multivers/data_verisci.py#L175

>         This function is needed because the data schema is designed so that each rationale can have its own support label. But, in the dataset, all rationales for a given claim / abstract pair all have the same label. So, we store the label at the "abstract level" rather than the "rationale level".

So we only allow either SUPPORTIN or REFUTING sentences from one combined wikipedia abstract

[^1]: Diggelmann, Thomas; Boyd-Graber, Jordan; Bulian, Jannis; Ciaramita, Massimiliano; 
Leippold, Markus (2020). CLIMATE-FEVER: A Dataset for Verification of Real-World Climate 
Claims. In: Tackling Climate Change with Machine Learning workshop at NeurIPS 2020, Online, 
11 December 2020 - 11 December 2020.
[^2]: Wadden, D., Lo, K., Wang, L.L., Cohan, A., Beltagy, I., & Hajishirzi, H. (2021). MultiVerS: Improving scientific claim verification with weak supervision and full-document context. NAACL-HLT.