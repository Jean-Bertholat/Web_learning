import React, { useEffect, useState } from 'react';

import {RegionInfoController} from '../controllers/region_info_controller';
import { RegionInfo } from '../services/schemas/region_resp_schema';

interface RegionInfoDisplayProps {
    regionId: number;
}

export const RegionInfoDisplay: React.FC<RegionInfoDisplayProps> = ({ regionId }) => {
    const regionService = RegionInfoController();
    const [regionInfo, setRegionInfo] = useState<RegionInfo | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchRegionInfo = async () => {
            try {
                const info = await regionService.get_region_info(regionId);
                setRegionInfo(info);
            } catch (err) {
                setError("Failed to fetch region information.");
            }
        };

        fetchRegionInfo();
    }, [regionId]);

    if (error) {
        return <div>{error}</div>;
    }

    if (!regionInfo) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h2>Region Information</h2>
            <p>ID: {regionInfo.id}</p>
            <p>Name: {regionInfo.name}</p>
            <p>Population: {regionInfo.nb_habitants}</p>
            <p>Language: {regionInfo.language}</p>
        </div>
    );
}  