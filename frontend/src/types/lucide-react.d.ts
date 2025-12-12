declare module 'lucide-react' {
    import { FC, SVGProps } from 'react';
    export interface IconProps extends SVGProps<SVGSVGElement> {
        size?: string | number;
        absoluteStrokeWidth?: boolean;
    }
    export type Icon = FC<IconProps>;
    export const LayoutDashboard: Icon;
    export const Globe: Icon;
    export const FolderOpen: Icon;
    export const Bell: Icon;
    export const Settings: Icon;
    export const Send: Icon;
    export const LogOut: Icon;
    export const ArrowRight: Icon;
    export const AlertTriangle: Icon;
    // Add other icons as needed or use a wildcard if lazy
    // export const [key: string]: Icon;
}

// Fallback for everything else
declare module 'lucide-react' {
    export * from 'lucide-react/dist/lucide-react';
}
