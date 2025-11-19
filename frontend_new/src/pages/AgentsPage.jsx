import {
  QueryClient,
  QueryClientProvider,
  useQuery,
} from '@tanstack/react-query'
import { API_BASE_URL } from '@/constants'
import AgentCard from '@/components/AgentCard'

const queryClient = new QueryClient()

export default function AgentsPage(){

    return (
        <QueryClientProvider client={queryClient}>
            <AgentsData/>
        </QueryClientProvider>
    )
}


function AgentsData() {

    // Queries
    const { isPending, error, data } = useQuery({ queryKey: ['agents'], queryFn: async () =>{
        const res = await fetch(`${API_BASE_URL}/agent`, {
            method: "GET",
            credentials: "include",
        })
        return res.json()
    } })

    if (isPending) return 'Loading...'

    if (error) return 'An error has occurred: ' + error.message

    return (
        <div>
            {data.map((agent) => (
            <AgentCard agent={agent}/>
            ))}
        </div>
    )
}