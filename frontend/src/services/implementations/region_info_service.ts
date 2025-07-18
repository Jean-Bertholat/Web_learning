import { IRegionService } from "../interfaces/Iregion_info_service";
import { RegionInfo } from "../schemas/region_resp_schema";


export class RegionInfoService1 implements IRegionService {
    private baseUrl: string;

    constructor(baseUrl: string = 'http://localhost:8000/api/v1') {
        this.baseUrl = baseUrl;
    }

    async get_region_info(region_id: number): Promise<RegionInfo> {
        const response = await fetch(`${this.baseUrl}/region/${region_id}`);
        if (!response.ok) {
            throw new Error('Failed to call backend');
        }
        return response.json();
    }
}


export class RegionInfoServiceMock implements IRegionService {
    async get_region_info(region_id: number): Promise<RegionInfo> {
        // Simulate fetching region info from an API or database
        return {
            id: region_id,
            name: "Mock Region",
            nb_habitants: 1000000,
            language: "English"
        };
    }
}
