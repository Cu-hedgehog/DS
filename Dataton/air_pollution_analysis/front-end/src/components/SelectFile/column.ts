export class ColumnDef{
    public field: string;
    public headerName: string;

    constructor(name: string){
        this.field = name;
        this.headerName = name;
    }
}