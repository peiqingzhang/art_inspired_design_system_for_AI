import type { Meta, StoryObj } from '@storybook/react';
import DataCard from './DataCard';

const meta  : Meta<typeof DataCard> = {
  title: 'Components/DataCard',
  component: DataCard,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof DataCard>;

export const Default: Story = { args={{ title: 'Metric', value: '1,234' }} };
export const WithTrend: Story = { args={{ title: 'Metric', value: '1,234', trend: 'up', trendValue: '12%' }} };
