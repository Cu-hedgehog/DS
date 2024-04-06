import { Button, Input, TextField } from "@mui/material";
import { InputNumber } from "../InputNumber/InputNumber";
import styles from '@/styles/Common.module.css';
import { changedAh, changedC6h6, changedHour, changedNmhc, changedNo2, changedNox, changedPt08Nmhc, changedPt08No2, changedPt08Nox, changedPt08O3, changedPt8Co, changedRh, changedT, changedWeekday, resetSingle, store } from "@/store/state-logic";
import { useEffect, useState } from "react";
import { InputMode } from "@/enums/modes";
import { RequestSender } from "@/services/request-sender";
import { Selector } from "../InputWeekDay/Selector";

export function InputDataModel(){
    let sender = new RequestSender()
    let initial = store.getState()['mode'] != InputMode.Manual 
    const [val, updateState] = useState(initial)
    const [result, setResult] = useState({val:0, isVisible: false})
    store.subscribe(() =>{
        let st = store.getState()['mode'] != InputMode.Manual
        console.log(val, st)
        updateState(st)
        console.warn(val)
    })

    const [canSend, setIsFull] = useState(false)

    store.subscribe(() =>{
        let state  = store.getState()['singleModel']
        let isFull = state['ah'] != undefined &&
            state['c6h6'] != undefined &&
            state['hour'] != undefined &&
            state['nmhc'] != undefined &&
            state['no2'] != undefined &&
            state['nox'] != undefined &&
            state['pt08Co'] != undefined &&
            state['pt08Nmhc'] != undefined &&
            state['pt08No2'] != undefined &&
            state['pt08Nox'] != undefined &&
            state['pt08O3'] != undefined &&
            state['t'] != undefined &&
            state['rh'] != undefined &&
            state['ah'] != undefined &&
            state['weekday'] != undefined &&
            state['hour'] != undefined
        setIsFull(isFull)
    })

    async function sendData(){
        setResult({val: 0, isVisible: false})
        let state = store.getState()
        let model = state['singleModel']
        let alghoritm = state['predictModel']
        let res = await sender.sendRequest(alghoritm, [model])
        setResult({val: res[0], isVisible: true})
        console.log(res)
    }


    let weekDays =['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    let hours =[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]

    return val ? <></> : <div className={styles.inputwindow} >
        <InputNumber header={"PT08.S1(CO)"} numberUpdated={data => store.dispatch(changedPt8Co({value: data}))}/>
        <InputNumber header={"NMHC(GT)"} numberUpdated={data => store.dispatch(changedNmhc({value: data}))}/>
        <InputNumber header={"C6H6(GT)"} numberUpdated={data => store.dispatch(changedC6h6({value: data}))}/>
        <InputNumber header={"PT08.S2(NMHC)	"} numberUpdated={data => store.dispatch(changedPt08Nmhc({value: data}))}/>
        <InputNumber header={"NOx(GT)"} numberUpdated={data => store.dispatch(changedNox({value: data}))}/>
        <InputNumber header={"PT08.S3(NOx)"} numberUpdated={data => store.dispatch(changedPt08Nox({value: data}))}/>
        <InputNumber header={"NO2(GT)"} numberUpdated={data => store.dispatch(changedNo2({value: data}))}/>
        <InputNumber header={"PT08.S4(NO2)"} numberUpdated={data => store.dispatch(changedPt08No2({value: data}))}/>
        <InputNumber header={"PT08.S5(O3)"} numberUpdated={data => store.dispatch(changedPt08O3({value: data}))}/>
        <InputNumber header={"T"} numberUpdated={data => store.dispatch(changedT({value: data}))}/>
        <InputNumber header={"RH"} numberUpdated={data => store.dispatch(changedRh({value: data}))}/>
        <InputNumber header={"AH"} numberUpdated={data => store.dispatch(changedAh({value: data}))}/>
        <Selector items={weekDays} header="Weekday" onChanged={data => store.dispatch(changedWeekday({value: data}))}/>
        <Selector items={hours} header="Hour" onChanged={data => store.dispatch(changedHour({value: data}))}/>
        <Button 
        disabled={!canSend}
        variant="contained" 
        size="large" 
        onClick={sendData} className={styles.sendButton}>Send</Button>
        { result.isVisible ?  <TextField
            label="Result"
            type="number"
            defaultValue={result.val}
            value={result.val}
            className={styles.inputRow}
            InputLabelProps={{
            shrink: true,
        }}/> : null}
       
    </div>
}