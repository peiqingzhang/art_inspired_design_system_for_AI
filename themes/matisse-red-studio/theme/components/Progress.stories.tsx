import type { Meta, StoryObj } from '@storybook/react';
import Progress from './Progress';

const meta  : Meta<typeof Progress> = {
  title: 'Components/Progress',
  component: Progress,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Progress>;

export const Linear: Story = { args={{ value: 65, variant: 'linear' }} };
export const Circular: Story = { args={{ value: 65, variant: 'circular' }} };
export const Indeterminate: Story = { args={{ indeterminate: true }} };
