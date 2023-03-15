export const ProgressBar = ({progressPercentage}) => {
    return (
        <div className='h-full w-full bg-gray-300 rounded-full'>
            <div
                style={{ width: `${progressPercentage}%`}}
                className={'h-full bg-green-600 rounded-l-full'}>
            </div>
            
        </div>
    );
};