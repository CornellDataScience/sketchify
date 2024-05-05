import { ReactNode } from "react";

type FileInputProps = {
  [key: string]: any;
};

const FileInput = ({ onChange, ...props }: FileInputProps) => {
  return (
    <div>
      <input
        onChange={onChange}
        className="block min-w-1/2 text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"
        id="file_input"
        type="file"
      />
    </div>
  );
};

export default FileInput;
