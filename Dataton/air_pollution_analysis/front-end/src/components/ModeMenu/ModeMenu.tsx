import { List, ListItemButton, ListItemText, MenuList } from "@mui/material";
import * as modes from '@/constants/menu-items'
import * as modesEnum from '@/enums/modes'
import React from "react";
import styles from '@/styles/Common.module.css'
import { store, modeChanged } from "@/store/state-logic";

export function ModeMenu(){
    const [selectedIndex, setSelectedIndex] = React.useState(0);
  
    const handleListItemClick = (event: any, index:number) => {
        store.dispatch(modeChanged({mode: index}))
        setSelectedIndex(index);
    };
    return <List className={styles.menu}>
        <ListItemButton className={selectedIndex == modesEnum.InputMode.Manual.valueOf() ? styles.menuSelected : styles.menuButton}
            selected ={selectedIndex == modesEnum.InputMode.Manual.valueOf()}
            onClick={(event) => handleListItemClick(event, modesEnum.InputMode.Manual.valueOf())}>
             <ListItemText  ><h3>{modes.SinglePrediction}</h3></ListItemText>
        </ListItemButton>
        <ListItemButton
            className={selectedIndex == modesEnum.InputMode.FromFile.valueOf() ? styles.menuSelected : styles.menuButton}
            selected ={selectedIndex == modesEnum.InputMode.FromFile.valueOf()}
            onClick={(event) => handleListItemClick(event, modesEnum.InputMode.FromFile.valueOf())}>
            <ListItemText ><h3>{modes.PredictionSet}</h3></ListItemText>
        </ListItemButton>
    </List>
}