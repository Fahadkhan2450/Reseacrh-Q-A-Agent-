class array{
    public static void main(string[] args){
        int[]arr={1,2,3,4,5,6,7,8};
        Scanner sc=new Scanner(System.in);

        system.out.print("Enter number to search: ");
        int key=sc.nextInt();

        boolean found=false;
        for(int i=0;i<arr.length;i++){
            if(arr[i]==key){
                system.out.print("found "+i);
                found=true;
                break;
            }
        }

        if(!found){
            System.out.println("Element not found");
        }

    }
}