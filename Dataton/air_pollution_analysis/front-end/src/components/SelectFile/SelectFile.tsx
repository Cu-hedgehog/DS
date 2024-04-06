import { InputMode } from '@/enums/modes';
import { addedHeaders, addedInputs, addedRows, clearInputs, store } from '@/store/state-logic';
import React, { CSSProperties, useState } from 'react';
import common from '@/styles/Common.module.css'
import { useCSVReader } from 'react-papaparse';
import { Button, TextField } from '@mui/material';
import { useFilePicker } from 'use-file-picker';
import Papa from 'papaparse';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { ColumnDef } from './column';
import { getRowIdFromRowModel } from '@mui/x-data-grid/internals';
import { RequestSender } from '@/services/request-sender';


export default function CSVReader() {
    let initial = store.getState()['mode'] != InputMode.FromFile 
    let sender = new RequestSender();
    const [val, updateState] = useState(initial)
    const [filName, updateFile] = useState("")
    const [isTableVisible, setTableVisibility] =useState(false);
    const [isSendAllowed, allowSend] =useState(false)
    const [rows, setRows] =useState([] as string[][])
    const [columns, setColumns] = useState([] as GridColDef[])
    store.subscribe(() =>{
        let st = store.getState()['mode'] != InputMode.FromFile
        console.log(val, st)
        updateState(st)
        console.warn(val)
    })
    async function send(){
      setTableVisibility(false)
      let state = store.getState()
      let model = state['inputs']
      let alghoritm = state['predictModel']
      let res = await sender.sendRequest(alghoritm, model)
      let stateUpdated = store.getState()
      let cols = stateUpdated['headersFromFile'].concat(["Co2"])
      let headers = cols.map(x => new ColumnDef(x))
      let rows = stateUpdated['inputs']
      let newRows = []
      for(let i=0; i< rows.length; ++i){
        let next : any ={} 
        for(let j=0; j<cols.length; ++j){
          next[cols[j]] = rows[i][cols[j]]
        }
        next['Co2'] = res[i]
        newRows.push(next)
      }
      setColumns(headers)
      setRows(newRows)
      setTableVisibility(true)
      allowSend(true)
      
    }
    const { openFilePicker, filesContent, loading, errors, plainFiles, clear } = useFilePicker({
        accept: '.csv',
        multiple: false,
        onFilesSelected: ({ plainFiles, filesContent, errors }) => {
          setTableVisibility(false)
          setColumns([])
          setRows([])
          allowSend(false)
          store.dispatch(clearInputs({}))
          store.dispatch(addedHeaders({headers: []}))
          store.dispatch(addedRows({data: []}))
          console.log(filesContent)
          updateFile(filesContent[0].name)
          let objects =[]
          let a =Papa.parse(filesContent[0].content)
          let header = a.data[0] as string[];
          let rows = (a.data as string[][]).slice(1, a.data.length)
          for(let i =0; i< rows.length; ++i){
            let next : any ={} 
            for(let j=0; j<header.length; ++j){
              next[header[j]] = Number.parseFloat(rows[i][j]) 
            }
            objects.push(next)
          }
          let headers = header.map(x => new ColumnDef(x))
          store.dispatch(addedInputs({inputs: objects}))
          store.dispatch(addedHeaders({headers: header}))
          store.dispatch(addedRows({data: rows}))
          setColumns(headers as GridColDef[])
          setRows(objects)
          setTableVisibility(true)
          allowSend(true)
        }
      });
    let id =0;
    return val ? <></> : <div className={common.inputwindow}>
        <TextField
          id="outlined-number"
          label="File name"
          defaultValue={filName}
          value={filName}
          placeholder="Select file..."
          className={common.input}
          InputLabelProps={{
          shrink: true,
        }}
        />
        <Button className={common.sendFileButton} onClick={() => openFilePicker()}>Select files</Button>
        <Button className={common.sendFileButton} disabled={!isSendAllowed} onClick={() => send()}>Send</Button>
      <br />
      <div hidden={!isTableVisible} style={{ 
        height: 600, 
        width: '100%',
        marginTop: 20 }}>
      <DataGrid
        rows={rows}
        columns={columns}
        getRowId={(row) => {id++; return id}}
        initialState={{
          pagination: {
            paginationModel: { page: 0, pageSize: 10 },
          },
        }}
        pageSizeOptions={[10, 20, 50, 100]}
        checkboxSelection
      />
    </div>
    </div>
}