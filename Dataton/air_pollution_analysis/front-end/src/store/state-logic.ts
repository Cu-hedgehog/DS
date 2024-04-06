import { Input } from "@/data-models/input"
import { InputMode } from "@/enums/modes"
import { PredictModels } from "@/enums/predict-models"
import { createSlice, configureStore } from '@reduxjs/toolkit'

let initList: any[] =[]
let headers: string[] =[]
const counterSlice = createSlice({
  name: 'prediction_monitor',
  initialState: {
    mode: InputMode.Manual,
    predictModel: PredictModels.boosting,
    inputs: initList,
    singleModel : new Input(),
    headersFromFile: headers,
    entities: []
  },
  reducers: {
    modeChanged: (state, params) => {
      state.mode = params.payload['mode']
    },
    predictModelChanged: (state, params) => {
      state.predictModel = params.payload['predictModel']
    },
    addedInput:(state, params)=>{
      state.inputs.push(params.payload['input'])
    },
    clearInputs:(state, params)=>{
      state.inputs =[]
    },
    resetSingle:(state, params)=>{
      state.singleModel = new Input()
    },
    addedInputs:(state, params)=>{
        state.inputs = params.payload['inputs']
      },
    changedPt8Co:(state, params) =>{
      state.singleModel.pt08Co = params.payload['value']
    },
    changedNmhc:(state, params) =>{
      state.singleModel.nmhc = params.payload['value']
    },
    changedC6h6:(state, params) =>{
      state.singleModel.c6h6 = params.payload['value']
    },
    changedPt08Nmhc:(state, params) =>{
      state.singleModel.pt08Nmhc = params.payload['value']
    },
    changedNox:(state, params) =>{
      state.singleModel.nox = params.payload['value']
    },
    changedPt08Nox:(state, params) =>{
      state.singleModel.pt08Nox = params.payload['value']
    },
    changedNo2:(state, params) =>{
      state.singleModel.no2 = params.payload['value']
    },
    changedPt08No2:(state, params) =>{
      state.singleModel.pt08No2 = params.payload['value']
    },
    changedPt08O3:(state, params) =>{
      state.singleModel.pt08O3 = params.payload['value']
    },
    changedT:(state, params) =>{
      state.singleModel.t = params.payload['value']
    },
    changedRh:(state, params) =>{
      state.singleModel.rh = params.payload['value']
    },
    changedAh:(state, params) =>{
      state.singleModel.ah = params.payload['value']
    },
    changedWeekday:(state, params) =>{
      state.singleModel.weekday = params.payload['value']
    },
    changedHour:(state, params) =>{
      state.singleModel.hour = params.payload['value']
    },
    addedHeaders:(state, params) =>{
      state.headersFromFile = params.payload['headers']
    },
    addedRows:(state, params) =>{
      state.entities =params.payload['data']
    }
  }
})

const store = configureStore({
  reducer: counterSlice.reducer
})
const { 
  modeChanged, 
  predictModelChanged, 
  addedInput, 
  addedInputs,
  changedPt8Co,
  changedNmhc,
  changedC6h6,
  changedPt08Nmhc,
  changedNox,
  changedPt08Nox,
  changedNo2,
  changedPt08No2,
  changedPt08O3,
  changedT,
  changedRh,
  changedAh,
  changedWeekday,
  changedHour,
  addedHeaders,
  addedRows,
  resetSingle,
  clearInputs} = counterSlice.actions
export {
  store, 
  modeChanged, 
  predictModelChanged, 
  addedInput, 
  addedInputs,
  changedPt8Co,
  changedNmhc,
  changedC6h6,
  changedPt08Nmhc,
  changedNox,
  changedPt08Nox,
  changedNo2,
  changedPt08No2,
  changedPt08O3,
  changedT,
  changedRh,
  changedAh,
  changedWeekday,
  changedHour,
  addedHeaders,
  addedRows, 
  resetSingle,
  clearInputs}


// Can still subscribe to the store
//store.subscribe(() => console.log(store.getState()))

// Still pass action objects to `dispatch`, but they're created for us
//store.dispatch(fileUploaded({name :'aaa'}))
// {value: 1}
//store.dispatch(incremented())
// {value: 2}
//store.dispatch(decremented())
// {value: 1}