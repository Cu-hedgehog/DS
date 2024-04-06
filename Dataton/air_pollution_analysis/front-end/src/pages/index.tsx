import Head from 'next/head'
import Image from 'next/image'
import { Inter } from 'next/font/google'
import styles from '@/styles/Common.module.css'
import { InputNumber } from '@/components/InputNumber/InputNumber'
import { ModeMenu } from '@/components/ModeMenu/ModeMenu'
import { PredictModelSelector } from '@/components/PredictModelSelector/PredictModelSelector'
import { InputDataModel } from '@/components/InputData/InputDataModel'
import SelectFile from '@/components/SelectFile/SelectFile'

const inter = Inter({ subsets: ['latin'] })

export default function Home() {
  return (
    <div className={styles.window}>
     <ModeMenu/>
     <div className={styles.modeWindow}>
        <PredictModelSelector/>
        <InputDataModel/>
        <SelectFile/>
     </div>
     
     
    </div>
  )
}
