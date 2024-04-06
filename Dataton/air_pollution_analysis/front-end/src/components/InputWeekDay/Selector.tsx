import { FormHelperText, MenuItem, Select, SelectChangeEvent, TextField } from "@mui/material";
import React from "react";
import styles from '@/styles/Common.module.css'
import { ISelectorProps } from "./props";

export function Selector(props: ISelectorProps){
    const [item, setItem] = React.useState(0);
    const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
        setItem(Number.parseInt(event.target.value));
        props.onChanged(Number.parseInt(event.target.value))
    };
    return <TextField
          select
          label={props.header}
          defaultValue={0}
          onChange={handleChange}
          className={styles.inputRow}
        >
          {props.items.map((option, index) => (
            <MenuItem key={index} value={index}>
              {option}
            </MenuItem>
          ))}
        </TextField> 
}