# Covid-19-Model
This repository contains project files for CoVID-19 Model built by Dalberg

## Technical paper on Dalberg&#39;s CoVID-19 Model

Various experts, statisticians, and businesses are working on a wide range of epidemiological models to gain deeper understanding of CoVID-19. Tools derived from such models can predict broader impact of the disease in a geography, identify right policy interventions and enable better allocation of resources.

The Dalberg model is unique due to two main reasons:

1. We have used a modified version of the standard SEIRS model to build our projection engine. These modifications allow the model to reflect **unique features of CoVID-19 disease** , such as being infectious without exhibiting any symptoms, and different disease reproduction rates for people with and without symptoms
2. By applying a machine-learning on top of the simulation engine, the model is capable of identifying &#39;dynamic&#39; parameters of the disease in near real-time and adjust the projections accordingly. This **helps create a &#39;sandbox mode&#39; for policy interventions** and observe their impact within few days of implementing an intervention

There are four steps involved in developing this model:

- **Step I** : Selecting the epidemiological model
- **Step II** : Developing differential equations governing shift of population through the disease cycle
- **Step III** : Understanding the nature of disease features
- **Step IV** : Building the simulation engine
- **Step V** : Building the Machine Learning layer for real time prediction


### **Step I: Selecting the epidemiological model**

We picked a generalised SEIRS epidemiological model with vital dynamics, and made two specific modifications to it (Figure 1).

- We consider two categories of people who can be infectious – those who do not display any symptoms or display only minor symptoms, and those who display severe symptoms1. The lack of obvious symptoms in infectious individuals is an important characteristic of the CoVID-19, also making it a very insidious disease and hence important to model
- We have split &#39;Removed&#39; into &#39;Recovered&#39; and &#39;Dead&#39; as these statistics are important for understanding the extent of casualty and for reliably using the ML algorithm, as we will explore.

###### *Figure 1: Schematic representing shift of population through SEIRS model of disease cycle, and subsequent CoVID-19 modifications*
![Covid19 Schematic](https://github.com/dalbergasia/Covid-19-Model/blob/master/images/schematic.jpg)

Please note that for any short-term projection, the vital dynamics components (i.e. birth and death rates) and disease recurrence rate, if any for CoVID-19, will have no reasonable impact. Additionally, the model assumes a closed system with no movement of people in and out of the system, except due to birth/death.

### **Step II: Developing differential equations governing shift of population through the disease cycle**

Aligned with the above schematic, we have following differential equations

<img src="https://github.com/dalbergasia/Covid-19-Model/blob/master/images/differential%20equations.jpg" height="250">

Where, at any given time,

- **N** is the total population
- **S** is part of the population that is susceptible to catching the disease
- **E** is part of the population that has been exposed to the virus, but hasn&#39;t become infectious yet
- **I** is part of the population that is infectious, but showing mild or no symptoms
- **C** is part of the population that is infectious with severe symptoms, requiring hospitalisation
- **R** is part of the population that has recovered from the disease
- **D** is population that has died due to the disease and is not a part of the population

And the parameters (described in terms of disease or demographic features) are,

<img src="https://github.com/dalbergasia/Covid-19-Model/blob/master/images/parameters_1.jpg" width="700">
<img src="https://github.com/dalbergasia/Covid-19-Model/blob/master/images/parameters_2.jpg" width="700">

### **Step III: Understanding the nature of disease features:**

Based on above description, the model requires 9 disease features as inputs. These features can be classified into two categories: six **static features** and three **dynamic features**.

- **Static features** are features of the disease that are mainly inherent to the disease itself and can remain largely unchanged across communities. Static nature of these features allows us to pick their values from global studies. However, it should be noted that these features may mutate in the future with the virus itself:

     | **Static disease features** | **Value** |
     | --- | :-: |
     | *Percentage of exposed who become infectious with severe symptoms* | 19% |
     | *Percentage of recovered population who may re-contract the virus* | 0% (unused) |
     | *Days an exposed person takes to become infectious* | 5 |
     | *Days for which a person with mild or no symptoms remains infectious before recovery* | 20 |
     | *Days for which a person with severe symptoms remains infectious before recovery or death* | 20 |
     | *Days before a recovered person re-contracts the virus* | 30 (unused) |

- **Dynamic features** are those disease features that also depend on community circumstances and can be heavily influenced by the way in which communities and governments respond to CoVID-19. We identify 3 such features:

  - **_Number of exposures caused by infectious people with mild or no symptoms:_** This is disease&#39;s basic reproduction rate for people showing mild symptoms, and can be influenced by community customs, population density, lockdowns, social-distancing, personal hygiene and usage of masks

  - **_Number of exposures caused by infectious people with severe symptoms:_** People showing severe symptoms may naturally have a higher disease reproduction rate, however they may also be easily identifiable. With a good quarantine mechanism in place, such people can be easily separated from the population, lowering their disease reproduction rate

  - **_Percentage of infectious people with severe symptoms who recover:_** This will depend on a community&#39;s comorbidity factors (e.g. high diabetes prevalence) and access to healthcare

Dynamic nature of these features along with model&#39;s high sensitivity towards them2 implies that values estimated in one location may not be used in another, and only measurements made in local and current context can provide reliable forecasts.

### **Step IV: Building the simulation engine**

Using the model equations from Step II and values of _static features_ from step III, we built a deterministic model in Python (WIP) and excel (Completed).  Figure 2 shows time variance of susceptible (S), Exposed (E), Infectious with mild symptoms (I), Infectious with severe symptoms (C), Recovered (R), and Dead (D) over the next 2-years for India, using three set of values for dynamic features. As indicated earlier, the projections of peak hospital requirement and total number of fatalities vary significantly across the three set

_Figure 2: Simulation model to be updated_

### **Step V: Building the Machine Learning layer for real time prediction**

Once we have the underlying simulation engine, in the next step we built a machine learning layer to figure out what set of values for the dynamic parameters best explains the real-world data. In other words, we try to find values of the dynamic features which best fits the projection curve on the real-world data.

Recognising lack of any standard R or Python library to run regression on custom models, such as those built using a modified SIERS, we have achieved the curve-fitting using first principle approach: We compare modelled values against the real-world data, estimate the overall error term, and allow disease features to vary within certain constraints with an objective to minimise this error term. This approach allows us to convert an ML problem into an Optimisation problem, where we try to find the minima of the error term in the _dynamic features_ plane. In excel, we implement this optimisation using the _solver add-on_ with GHG-Non-Liner algorithm. In Python (WIP), we take a brute-force approach. With just 3 dynamic features that can vary in small ranges, efficiency of calculation with brute-force was not found to be an issue. However, there remains a scope to make optimisation algorithm in python significantly more efficient.

For this curve-fitting exercise, we select two most commonly available daily data feeds for most countries (note that other real-world data feeds, such as number of hospitalised CoVID-19 cases, if it reliably reflects all severe cases, can also be used for this exercise):

1. Daily number of CoVID-19 deaths
2. Daily identified cases of CoVID-19

_A note on the overall Error term_

**Including multiple data feeds:** While, reported number of CoVID-19 deaths can be one of the most reliable data feeds, in a country such as Singapore with only 4 deaths3, it may also lack any statistical power. On the other hand, large number of daily identified cases can provide the required statistical power but may also be under-reported. To solve for this, we estimate overall error terms by assigning pre-specified weights to the normalised version of respective errors in the two data feeds. These weights reflect our preference (and trust) for the data feed to be used in fitting the curve.

 Where,

represents number of days before today for the data point;  is square error for the ith previousday from today in number of deaths;  is square error for the ith previousday from today in number of cases; is weight assigned to the number of deaths data feed; is weight assigned to the number of cases data feed

**Building a recency bias:** Additionally, Given that the situation is rapidly evolving, including awareness amongst people toward social distancing and personal hygiene, and governments&#39; efforts, we also wanted to ensure that the ML model gives more weightage to recent data points compared to older data points. For this we have implemented a slow exponential reduction, where each previous day has 90% weightage than the subsequent day. Using this factor, the weight reduces to 60% for 5th previous day, 37% for 10th previous day, and 5% for 30th previous day compared to today.

**Results (so far):**

**For Singapore: TBU**

**For India: TBU**

**Next steps:**

- Finetuning the values of static features using global data
- Extensive testing and feedback
- Develop deployable versions that can be picked by local and state governments to test interventions


-----------
<a name="1">1</a>: Severe symptoms: We define this group as those who require hospital care for oxygen or ICU support
<a name="2">1</a>: Note on sensitivity of disease prediction against reproduction rates
<a name="3">1</a>: As on 2nd April 2020



