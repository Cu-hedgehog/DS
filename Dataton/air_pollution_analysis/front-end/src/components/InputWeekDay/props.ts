export interface ISelectorProps{
    items: any[],
    header: string,
    onChanged(val: number): void
}