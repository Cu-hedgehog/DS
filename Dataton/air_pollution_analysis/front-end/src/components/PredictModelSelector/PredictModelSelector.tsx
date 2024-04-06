import { Direction, FormControlLabel, Radio, RadioGroup, ToggleButton, ToggleButtonGroup } from "@mui/material";
import { PredictModels } from "@/enums/predict-models";
import React from "react";
import { predictModelChanged, store } from "@/store/state-logic";
import * as predictors from '@/constants/prediction-model'
import styles from '@/styles/Common.module.css'

export function PredictModelSelector(){

    const [value, setValue] = React.useState(PredictModels.boosting);
  
    const handleRadioChange = (event: React.MouseEvent<HTMLElement, MouseEvent>) => {
      let val = (event.target as HTMLInputElement).value as PredictModels
      setValue(val);
      store.dispatch(predictModelChanged({predictModel: val}))
    };
    return <ToggleButtonGroup
        className={styles.predictMode}
        defaultValue={PredictModels.boosting}
        onChange={handleRadioChange}>
            <ToggleButton 
                className={value == PredictModels.boosting ? styles.clicked : styles.button}
                value={PredictModels.boosting} 
                selected={value == PredictModels.boosting}>
                    {predictors.Boosting}
            </ToggleButton>
            <ToggleButton 
                className={value == PredictModels.forest ? styles.clicked : styles.button}
                value={PredictModels.forest} 
                selected={value == PredictModels.forest}>
                    {predictors.Forest}
            </ToggleButton>
            <ToggleButton 
                className={value == PredictModels.knn ? styles.clicked : styles.button}
                value={PredictModels.knn}
                selected={value == PredictModels.knn}>
                    {predictors.Knn}
            </ToggleButton>
            <ToggleButton 
                className={value == PredictModels.lasso ? styles.clicked : styles.button}
                value={PredictModels.lasso } 
                selected={value == PredictModels.lasso}> 
                    {predictors.Lasso}
            </ToggleButton>
            <ToggleButton 
                className={value == PredictModels.linear ? styles.clicked : styles.button}
                value={PredictModels.linear } 
                selected ={value == PredictModels.linear}>
                    {predictors.Linear}
            </ToggleButton>
            {/*<ToggleButton 
                className={value == PredictModels.neural ? styles.clicked : styles.button}
                value={PredictModels.neural } 
                selected={value == PredictModels.neural}> 
                    {predictors.Neural}
            </ToggleButton>*/}
            <ToggleButton 
                className={value == PredictModels.svr ? styles.clicked : styles.button}
                value={PredictModels.svr } 
                selected ={value == PredictModels.svr}>
                    {predictors.Svr}
            </ToggleButton>
  </ToggleButtonGroup>
}